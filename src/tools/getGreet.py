import logging
from logging_config import setup_logging

setup_logging()

class GetGreet:
    def __init__(self):
        logging.info("GetGreet initialized with URL")

    def get_greet(self, query:str):
        try:
            return f"Hey! I'm here to make things easier for you. How can I be of service?"
        
        except Exception as e:
            logging.error(f"Error processing query '{query}': {e}")
            return "There was an error processing your request. Please try again later."

