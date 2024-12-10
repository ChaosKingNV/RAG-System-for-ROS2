from transformers import AutoTokenizer
import torch
import json
from torch.utils.data import Dataset

class LabeledDataset(Dataset):
    def __init__(self, data_file, tokenizer_name="facebook/bart-large", max_len=512):
        self.data = self.load_data(data_file)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.max_len = max_len

    def load_data(self, data_file):
        with open(data_file, "r") as f:
            return json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        inputs = self.tokenizer(
            item["question"], 
            item["answer"], 
            max_length=self.max_len, 
            padding="max_length", 
            truncation=True, 
            return_tensors="pt"
        )

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": torch.tensor(1)  # For binary classification
        }
