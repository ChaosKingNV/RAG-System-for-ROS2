import os
from pymongo import MongoClient
from qdrant_client import QdrantClient
from clearml import Task
from transformers import pipeline

# MongoDB Connection Test
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.admin.command("ping")  # Check if MongoDB is reachable
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

# Qdrant Connection Test
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
try:
    qdrant_client = QdrantClient(url=QDRANT_URL)
    print("✅ Connected to Qdrant")
except Exception as e:
    print(f"❌ Qdrant connection failed: {e}")

# ClearML Task Test
try:
    task = Task.init(project_name="Test Project", task_name="Test Task")
    print("✅ Connected to ClearML")
except Exception as e:
    print(f"❌ ClearML initialization failed: {e}")

# Hugging Face Pipeline Test
try:
    hf_pipeline = pipeline("sentiment-analysis")
    result = hf_pipeline("Hello, world!")
    print(f"✅ Hugging Face Pipeline Test Passed: {result}")
except Exception as e:
    print(f"❌ Hugging Face pipeline failed: {e}")
