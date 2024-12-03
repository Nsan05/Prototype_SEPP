from datasets import load_dataset, Dataset

#load data
data_path = "recipes.json"
dataset = load_dataset("json", data_files=data_path)