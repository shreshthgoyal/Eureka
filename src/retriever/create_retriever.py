import logging
from logging_config import setup_logging
import os
import dotenv
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from src.retriever.config import RETRIEVER_K

setup_logging()
dotenv.load_dotenv()

class CreateRetriever:
    def __init__(self, vector_db=None):
        self.vector_db = vector_db

    def get_metadata(self, query:str):
        try:
            docs = self.vector_db.similarity_search(query)
            return docs[0].metadata
        
        except Exception as e:
            logging.error(f"Error getting metadata: {e}")
            raise
    
    def search_similar(self, query:str):
        try:
            docs = self.vector_db.similarity_search(query)
            return docs[0].page_content
        
        except Exception as e:
            logging.error(f"Error getting page_content: {e}")
            raise
    
    def get_retriever(self):
        if self.vector_db is None:
            raise ValueError("Vector DB is not provided")
        
        retriever = self.vector_db.as_retriever(search_type="mmr", search_kwargs={"k": RETRIEVER_K})
        return retriever
        # compressor = CohereRerank()
        # logging.info("Cohere Reranking")
        # compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
        # return compression_retriever


