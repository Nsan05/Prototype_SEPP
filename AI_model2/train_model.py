from datasets import load_dataset, Dataset
import json


#load data
data_path = "recipes.json"
with open(data_path, 'r') as f:
    raw_data = json.load(f)


#extraction of ingredients
def extract_ingredient_features(ingredient, recipe_name):
    #normalize quanitty
    def normalize_quantity(qty):
        try:
            numeric_value = float(re.sub(r'[^\d.]', '', str(qty))) #account for ml..
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

#more feautures
def prepare_dataset(raw_data):
    prepared_data = []
    for recipe in raw_data:
        for ingredient in recipe['ingredients']:
            prepared_data.append(extract_ingredient_features(ingredient, recipe['recipe_name']))
    return prepared_data


dataset = prepare_dataset(raw_data)
dataset = Dataset.from_list(dataset)

#mapping importance levels to ints
labels = {"core": 0, "secondary": 1, "optional": 2}
dataset = dataset.map(lambda x: {"label": labels[x["label"]]})

#train and test data
train_test_split = dataset.train_test_split(test_size=0.2)
train_data = train_test_split["train"]
test_data = train_test_split["test"]

#calculate weights
class_weights = compute_class_weight('balanced',classes=np.unique(train_data['label']), y=train_data['label'])
class_weights = torch.tensor(class_weights, dtype=torch.float)

#tokenization
model_name = "roberta-base"  #different model due to other model failures
tokenizer =AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)


def tokenize_function(examples):
    return tokenizer(
        examples["base_text"], truncation=True, 
        padding=True, max_length=128, add_special_tokens=True
    )

train_data = train_data.map(tokenize_function, batched=True)
test_data = test_data.map(tokenize_function, batched=True)