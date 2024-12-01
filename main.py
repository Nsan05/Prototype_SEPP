import psycopg2
from typing import Dict,Any
import logging
import ast

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

    def get_ingredient_names(self) -> Dict[int, str]:
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT ingredient_id, ingredient_name FROM ingredient"
                cursor.execute(query)
                return dict(cursor.fetchall())
        except psycopg2.Error as e:
            logging.error(f"Database error in get_ingredient_names: {e}")
            return {}
        
    def get_recipes(self) -> Dict[int, Dict[str, Any]]:
        try:
            with self.db_connection.cursor() as cursor:
                query = """
                    SELECT recipe_id, recipe_name, ingredient_list
                    FROM recipe
                """
                cursor.execute(query)
                recipes_data = cursor.fetchall()

            recipes = {}

            for recipe_id, recipe_name, ingredient_list_str in recipes_data:
                logging.info(f"Processing recipe {recipe_id}: {recipe_name}")

                try:
                    ingredient_list = ast.literal_eval(ingredient_list_str)
                except (ValueError, SyntaxError) as e:
                    logging.error(f"Error parsing ingredient list for recipe {recipe_id}: {e}")
                    continue

                core = {}
                secondary = {}
                optional = {}

                for ingredient_id, ingredient_data in ingredient_list.items():
                    try:
                        ingredient_id = int(ingredient_id)
                        ingredient_quantity, importance_level = ingredient_data[:2]

                        if importance_level == "core":
                            core[ingredient_id] = ingredient_quantity
                        elif importance_level == "secondary":
                            secondary[ingredient_id] = ingredient_quantity
                        elif importance_level == "optional":
                            optional[ingredient_id] = ingredient_quantity
                        else:
                            logging.warning(f"Unknown importance level {importance_level} for ingredient {ingredient_id}")

                    except Exception as e:
                        logging.error(f"Unexpected error processing ingredient {ingredient_id} in recipe {recipe_id}: {e}")

                recipes[recipe_id] = {
                    'recipe_name': recipe_name,
                    'core': core,
                    'secondary': secondary,
                    'optional': optional
                }

                logging.info(f"Recipe {recipe_id} processed successfully")

            return recipes
        except psycopg2.Error as e:
            logging.error(f"Database error in get_recipes: {e}")
            return {}    