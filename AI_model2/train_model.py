from datasets import load_dataset, Dataset
import json


#load data
data_path = "recipes.json"
with open(data_path, 'r') as f:
    raw_data = json.load(f)


#extraction of ingredients
def extract_ingredient_features(ingredient, recipe_name):
    def normalize_quantity(qty):
        try:
            numeric_value = float(re.sub(r'[^\d.]', '', str(qty))) #handle the quantity to take the numeric value
            return numeric_value
        except ValueError:
            return 0.0

    features = {
        "base_text": f"{ingredient['quantity']} of {ingredient['ingredient_name']} in {recipe_name}",
        "normalized_quantity": normalize_quantity(ingredient['quantity']),
        "ingredient_name_length": len(ingredient['ingredient_name']),
        "label": ingredient['importance']
    }
    return features
