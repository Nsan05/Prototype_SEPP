from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import json
import re

# label
label_map = {0:"core", 1:"secondary",2:"optional"}

#loading
# model_path = "./AI_model_roberta_saved" #testing roberta
model_path = "./AI_model_distilbert_saved" #testing distilbert
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

#classifier
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)


#normalize and accomodate quantity
def normalize_quantity(qty):
    try:
        return float(re.sub(r'[^\d.]', '', str(qty)))
    except ValueError:
        return 0.0

#loading test recipe
test_recipe_path = "test_recipe.json"
with open(test_recipe_path, "r") as f:
    test_recipe = json.load(f)


with open("recipes.json", "r") as f:
    training_recipes = json.load(f)

#classification of ingredients
for recipe in test_recipe:
    print(f"Recipe: {recipe['recipe_name']}")
    for ingredient in recipe["ingredients"]:
        ingredient_text = f"{ingredient['quantity']} of {ingredient['ingredient_name']} in {recipe['recipe_name']}"
        result = classifier(ingredient_text)
        
        # mapping label
        predicted_label = label_map[int(result[0]["label"].replace("LABEL_",""))]
        actual_label = ingredient["importance"]

        #matching
        match_status = "MATCH" if predicted_label.lower() == actual_label else "MISMATCH"
        print(
            f"'{ingredient_text}' -> Predicted: {predicted_label}, Actual: {actual_label} ({match_status})"
        )