import logging
from logging_config import setup_logging

setup_logging()

class PriceRetriever:
    def __init__(self):
        # self.urls = {
        #     "elite": "curefit://fl_listpage?pageId=Elite_lp_sale&hideTitle=true",
        #     "pro": "curefit://fl_listpage?pageId=Elite_lp_sale&hideTitle=true",
        #     "default": "curefit://fl_listpage?pageId=Elite_lp_sale&hideTitle=true"
        # }
        logging.info("PriceRetriever initialized with URLs")

    def get_price(self, query: str):
        try:
            # query_lower = query.lower()
            # logging.info(f"Received query: {query}")
            
            # if 'elite' in query_lower:
            #     logging.info("Query matched 'elite'")
            #     return f"You can see the details here: {self.urls['elite']}"
            # elif 'pro' in query_lower:
            #     logging.info("Query matched 'pro'")
            #     return f"You can see the details here: {self.urls['pro']}"
            
            # logging.info("Query matched 'default'")
            return f"You can see the details here."
        
        except Exception as e:
            logging.error(f"Error processing query '{query}': {e}")
            return "There was an error processing your request. Please try again later."
