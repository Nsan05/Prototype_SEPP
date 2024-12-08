from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# label
label_map = {0:"core", 1:"secondary",2:"optional"}

#loading
model_path = "./AI_model2"
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
    