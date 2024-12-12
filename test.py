import pytest
from main import RecipeSuggestion

# # Credentials for dockerised setup
db_params = {
    "dbname": "recipe_db",
    "user": "SEPP",
    "password": "prototype",
    "host": "localhost",
    "port": "5432"
}

