from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import torch
import json
import re


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
        "base_text": f"{ingredient['ingredient_name']} is a {ingredient['importance']} ingredient in {recipe_name}",
        # "base_text": f"{ingredient['quantity']} of {ingredient['ingredient_name']} in {recipe_name}",
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
# train_test_split = dataset.train_test_split(test_size=0.2)
# train_data = train_test_split["train"]
# test_data = train_test_split["test"]
#debug-using same data for test and train
train_data = dataset
test_data = dataset

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

#metrics calc
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions =np.argmax(logits, axis=-1)
    return {"accuracy":np.mean(predictions == labels)}

#define trainer
class EnhancedTrainer(Trainer):
    def training_step(self, model, inputs, *args, **kwargs): #to override original
        labels = inputs.get("labels")
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits
        
        loss_fct = torch.nn.CrossEntropyLoss(weight=class_weights.to(logits.device))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        
        return loss
    
training_args = TrainingArguments(
    output_dir="./AI_model_roberta",
    evaluation_strategy="steps",
    save_steps=50,
    eval_steps=50,
    learning_rate=2e-5, #switch to diff values later to accomodate
    per_device_train_batch_size=4,
    num_train_epochs=15,
    weight_decay=0.02,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="eval_accuracy", 
    greater_is_better=True
)

trainer = EnhancedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data,
    compute_metrics=compute_metrics, 
)

# train
trainer.train()
model.save_pretrained("./AI_model_roberta_saved")
tokenizer.save_pretrained("./AI_model_roberta_saved")

print("Roberta Base MODEL TRAINING COMPLETE")


#accuracy try1- 50.9, try 2- 13.5