import os
from pymongo import MongoClient
from qdrant_client import QdrantClient
from clearml import Task
from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import threading
import time

# FastAPI app setup
app = FastAPI()

# MongoDB Connection Test
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_client = None
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.admin.command("ping")  # Check if MongoDB is reachable
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

# Qdrant Connection Test
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_client = None
try:
    qdrant_client = QdrantClient(url=QDRANT_URL)
    print("✅ Connected to Qdrant")
except Exception as e:
    print(f"❌ Qdrant connection failed: {e}")

# ClearML Task Test
task = None
try:
    task = Task.init(project_name="Test Project", task_name="Test Task")
    print("✅ Connected to ClearML")
except Exception as e:
    print(f"❌ ClearML initialization failed: {e}")

# Hugging Face Pipeline Test
hf_pipeline = None
result = None
try:
    hf_pipeline = pipeline("sentiment-analysis")
    result = hf_pipeline("Hello, world!")
    print(f"✅ Hugging Face Pipeline Test Passed: {result}")
except Exception as e:
    print(f"❌ Hugging Face pipeline failed: {e}")

# API endpoint for testing the status of connections
class StatusResponse(BaseModel):
    mongo: str
    qdrant: str
    clearml: str
    huggingface: str

@app.get("/status", response_model=StatusResponse)
def get_status():
    return {
        "mongo": "Connected" if mongo_client else "Failed",
        "qdrant": "Connected" if qdrant_client else "Failed",
        "clearml": "Initialized" if task else "Failed",
        "huggingface": f"Test Passed: {result[0]['label']}" if result else "Failed"
    }

# Background task to keep connections alive (optional, for long-running processes)
def keep_alive():
    while True:
        # You can add periodic checks or keep-alive tasks here
        print("⚡ Checking connections...")
        try:
            # MongoDB health check
            if mongo_client:
                mongo_client.admin.command("ping")
            # ClearML health check
            if task:
                task.update_task_status()
        except Exception as e:
            print(f"❌ Error in keep_alive: {e}")
        
        time.sleep(60)  # Keep the process running and check every minute

# Run the keep_alive function in the background
thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()

# Start the FastAPI server if the script is run directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
