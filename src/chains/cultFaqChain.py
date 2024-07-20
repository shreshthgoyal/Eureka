import logging
from logging_config import setup_logging
import os
import dotenv
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from src.chains.config import CHAT_MODEL_NAME, CULT_TEMPLATE_STR
from langchain_fireworks import Fireworks
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


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
            
            contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            
            self.history_aware_retriever = create_history_aware_retriever(
                self.chat_model, retriever, contextualize_q_prompt
            )
    
            qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            
            
            question_answer_chain = create_stuff_documents_chain(self.chat_model, qa_prompt)

            self.rag_chain = create_retrieval_chain(self.history_aware_retriever, question_answer_chain)

            
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
        response = self.rag_chain.invoke({"input": query, "chat_history": self.history})
        self.history.extend([HumanMessage(content=query)])
        print(response)
        return response["context"][0].page_content
