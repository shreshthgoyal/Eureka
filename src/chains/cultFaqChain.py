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
# from langchain_cohere import ChatCohere

setup_logging()
dotenv.load_dotenv()

class CultFAQChain:
    def __init__(self, retriever):
        try:
            # self.chat_model = ChatGroq(groq_api_key=os.getenv('GROQ_API_KEY'), model_name=CHAT_MODEL_NAME)
            self.chat_model = Fireworks(
            model=CHAT_MODEL_NAME,
            )
            # self.chat_model = Ollama(model="mistral")
            self.cult_system_prompt = SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["context"],
                    template=CULT_TEMPLATE_STR,
                )
            )

            self.cult_human_prompt = HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["question"],
                    template="{question}",
                )
            )

            self.messages = [self.cult_system_prompt, self.cult_human_prompt]

            self.cult_prompt_template = ChatPromptTemplate(
                input_variables=["context", "question"],
                messages=self.messages,
            )

            self.cult_faq_chain = self.create_faq_chain(retriever)
            
            logging.info("CultFAQChain initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing CultFAQChain: {e}")
            raise


    def create_faq_chain(self, retriever):
        try:
            faq_chain = {
                "context": retriever,
                "question": RunnablePassthrough()
            } | self.cult_prompt_template | self.chat_model | StrOutputParser()
            return faq_chain
        except Exception as e:
            logging.error(f"Error creating FAQ chain: {e}")
            raise

    def get_chain(self):
        try:
            return self.cult_faq_chain
        except Exception as e:
            logging.error(f"Error retrieving FAQ chain: {e}")
            raise

    def invoke_chain(self, query:str): 
        response = self.cult_faq_chain.invoke({"input": query})
        return response
