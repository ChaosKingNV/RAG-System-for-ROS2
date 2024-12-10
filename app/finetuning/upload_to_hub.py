from huggingface_hub import HfApi, HfFolder, Repository
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from .config import CONFIG

def upload_model_to_hub(model_dir="finetuned_model", repo_name="ChaosKingNV/finetuned-ros2-model"):
    """
    Uploads the trained model to Hugging Face Hub.
    """
    # Authenticate with Hugging Face Hub
    token = os.getenv("HF_TOKEN")  # Hugging Face token should be stored as an environment variable
    if not token:
        raise ValueError("❌ Hugging Face token not found. Please set HF_TOKEN as an environment variable.")

    # Push Model to Hugging Face Hub
    print(f"🔧 Uploading model to repository: {repo_name}")
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["model_name"])

    model.push_to_hub(repo_name, use_auth_token=token)
    tokenizer.push_to_hub(repo_name, use_auth_token=token)

    print(f"✅ Model uploaded successfully to {repo_name}")