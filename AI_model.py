import pandas as pd
import numpy as np

# load dataset function
def load_data(file_path):
    return pd.read_csv(file_path)

#preprocess the data 
# for each recipe everything is inside one dictionary
def preprocess_data(df):
    #grouping
    recipe_ingredients = df.groupby('recipe_name').apply(lambda x: {
        'ingredients': x['ingredient_name'].tolist(),
        'quantities': x['quantity'].tolist(),
        'importance_levels': x['importance'].tolist()
    }).reset_index(name="recipe_data")
    
    return recipe_ingredients

#each column 
# def preprocess_data(df):
#     # Grouping by 'recipe_name' and aggregating the 'ingredient_name', 'importance', and 'quantity' columns
#     recipe_ingredients = df.groupby('recipe_name').agg(
#         ingredients=('ingredient_name', list),
#         quantities=('quantity', list),
#         importance_levels=('importance', list)
#     ).reset_index()
    
#     return recipe_ingredients

def main():
    df = load_data('ingredient_dataset.csv')
    recipe_ingredients = preprocess_data(df)
    recipe_ingredients.to_csv('output_filename.csv', index=False)

    # print(recipe_ingredients)
    x=0
    for index, row in recipe_ingredients.iterrows():
        if x==3:
            break
        print("***INDEX: ",index,"***ROW: ",row, sep="\n")
        print("BREAKER*************************")
        ingredients = row[1]['ingredients']
        print(ingredients)
        x+=1


# pd.set_option('display.max_columns', None) 
# pd.set_option('display.max_rows', None)     
# pd.set_option('display.max_colwidth', None)
main()
