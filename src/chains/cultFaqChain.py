import logging
from logging_config import setup_logging
import os
import dotenv
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from src.chains.config import CHAT_MODEL_NAME, CULT_TEMPLATE_STR
from langchain_fireworks import Fireworks

setup_logging()
dotenv.load_dotenv()

class DocumentFAQChain:
    def __init__(self, retriever):
        try:
            self.chat_model = Fireworks(model=CHAT_MODEL_NAME)
            self.system_prompt = SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["context"],
                    template=CULT_TEMPLATE_STR,
                )
            )

            self.human_prompt = HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["question"],
                    template="{question}",
                )
            )

            self.messages = [self.system_prompt, self.human_prompt]

            self.prompt_template = ChatPromptTemplate(
                input_variables=["context", "question"],
                messages=self.messages,
            )

            self.faq_chain = self.create_faq_chain(retriever)
            self.history = []
            
            logging.info("DocumentFAQChain initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing DocumentFAQChain: {e}")
            raise

    def create_faq_chain(self, retriever):
        try:
            faq_chain = {
                "context": retriever,
                "question": RunnablePassthrough()
            } | self.prompt_template | self.chat_model | StrOutputParser()
            return faq_chain
        except Exception as e:
            logging.error(f"Error creating FAQ chain: {e}")
            raise

    def get_chain(self):
        try:
            return self.faq_chain
        except Exception as e:
            logging.error(f"Error retrieving FAQ chain: {e}")
            raise

    def invoke_chain(self, query: str):
        self.history.append(query)
        context = " ".join(self.history)
        response = self.faq_chain.invoke({"context": context, "question": query})
        self.history.append(response)
        return response
