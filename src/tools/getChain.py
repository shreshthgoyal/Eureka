import logging
from logging_config import setup_logging
from src.chains.cultFaqChain import CultFAQChain


setup_logging()

class GetChain:
    def __init__(self, retriever):
        self.chain_instance = CultFAQChain(retriever)
        self.chain = self.chain_instance.get_chain()
        self.retriever = retriever
        logging.info(f"Chain Initialised successfully")

    def get_chain(self, query: str):
        try:
            logging.info(f"Received query: {query}")
            # response =  self.retriever.search_similar(query)
            response = self.chain.invoke(query)
            # return self.chain
            return response
        except Exception as e:
            logging.error(f"Error processing query '{query}': {e}")
            return "There was an error processing your request. Please try again later."

