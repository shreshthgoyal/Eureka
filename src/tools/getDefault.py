import logging
from logging_config import setup_logging

setup_logging()

class GetDefault:
    def __init__(self):
        logging.info("GetDefault initialized with URL")

    def get_default(self, query:str):
        try:
            logging.info(f"Received query: {query}")
            return f"I can't answer the provided query.)"
        except Exception as e:
            logging.error(f"Error processing query '{query}': {e}")
            return "There was an error processing your request. Please try again later."

