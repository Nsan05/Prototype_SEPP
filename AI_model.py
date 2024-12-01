import pandas as pd
import numpy as np

# load dataset function
def load_data(file_path):
    return pd.read_csv(file_path)

#preprocess the data 
def preprocess_data(df):
    #grouping
    recipe_ingredients = df.groupby('recipe_name').apply(lambda x: {
        'ingredients': x['ingredient_name'].tolist(),
        'quantities': x['quantity'].tolist(),
        'importance_levels': x['importance'].tolist()
    }).reset_index()
    
    return recipe_ingredients
 
def extract_features(recipe_ingredients):
    vectorizer = CountVectorizer()
    ingredient_features = vectorizer.fit_transform(
        [' '.join(ingredients) for ingredients in recipe_ingredients['ingredients']] #matrix
    )