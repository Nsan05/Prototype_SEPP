from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# label
label_map = {0:"core", 1:"secondary",2:"optional"}

#loading
model_path = "./AI_model2"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

#classifier
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)