# app/featurization/mongo_reader.py

from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import os

BATCH_SIZE = 500  

def clean_text(content):
    """
    Cleans text by removing HTML tags, special characters, and extra spaces.
    """
    # Remove HTML tags
    clean_text = BeautifulSoup(content, "html.parser").get_text(separator=" ")

    # Remove special characters & numbers
    clean_text = re.sub(r"[^a-zA-Z\s]", "", clean_text)

    # Remove extra spaces
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return clean_text


def fetch_and_clean_documents_in_batches(collection_name, batch_size=BATCH_SIZE):
    """
    Fetches documents from MongoDB in batches and cleans the text content.
    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/")
    client = MongoClient(MONGO_URI)
    db = client["rag_system"]
    collection = db[collection_name]

    total_docs = collection.count_documents({})
    print(f"📊 Found {total_docs} documents in '{collection_name}'.")

    for i in range(0, total_docs, batch_size):
        documents = list(collection.find({}, {"_id": 0}).skip(i).limit(batch_size))

        cleaned_docs = []
        for doc in documents:
            doc["content"] = clean_text(doc["content"])
            cleaned_docs.append(doc)

        print(f"✅ Cleaned {len(cleaned_docs)} documents from '{collection_name}'.")
        yield cleaned_docs
