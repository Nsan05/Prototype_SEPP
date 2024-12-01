import pandas as pd
import numpy as np

# load dataset function
def load_data(file_path):
    return pd.read_csv(file_path)

#preprocess the data 
def preprocess_data(df):
    # Group by recipe and aggregate ingredient information
    recipe_ingredients = df.groupby('recipe_name').apply(lambda x: {
        'ingredients': x['ingredient_name'].tolist(),
        'quantities': x['quantity'].tolist(),
        'importance_levels': x['importance'].tolist()
    }).reset_index()
    
    return recipe_ingredients
