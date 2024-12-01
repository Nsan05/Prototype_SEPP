import psycopg2
from typing import Dict
import logging

class RecipeSuggestion:
    def __init__(self, db_params: Dict[str, str], user_id: int):
        
        try:
            self.db_connection = psycopg2.connect(**db_params)
            self.db_connection.autocommit = True
            self.user_id = user_id
            self.alternatives = self.get_alternatives()
            self.ingredient_names = self.get_ingredient_names()
        except (Exception, psycopg2.Error) as error:
            logging.error(f"Error connecting to database: {error}")
            raise
