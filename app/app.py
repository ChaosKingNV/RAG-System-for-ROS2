from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests

# Import ETL and Featurization Pipelines
from etl.etl_pipeline import run_etl_pipeline
from featurization.featurization_pipeline import run_featurization_pipeline

# Import YouTube Data Pipelines
from youtube_pipeline.youtube_transcript_collector import fetch_youtube_transcripts
from youtube_pipeline.question_answer_generator import generate_labeled_data
from youtube_pipeline.config import VIDEO_IDS, TRANSCRIPTS_FILE, LABELED_DATA_FILE

# Import Fine-Tuning Pipeline
from finetuning.data_preprocessor import LabeledDataset
from finetuning.model_trainer import train_model
from finetuning.upload_to_hub import upload_model_to_hub
from finetuning.config import CONFIG

# Import ClearML Tracker
from clearml_integration.clearml_tracker import register_model_with_clearml

# Initialize FastAPI
app = FastAPI(
    title="AI Project API",
    description="API for ETL, Featurization, YouTube, Fine-Tuning, and System Check Pipelines",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint
@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the AI Project API!"}

# ETL Endpoint
@app.post("/run_etl")
def trigger_etl():
    """Triggers the ETL pipeline."""
    result = run_etl_pipeline()
    return {"status": "success", "details": result}

# Featurization Endpoint
@app.post("/run_featurization")
def trigger_featurization():
    """Triggers the Featurization pipeline."""
    result = run_featurization_pipeline()
    return {"status": "success", "details": result}

# Fetch YouTube Transcripts Endpoint
@app.post("/fetch_youtube_transcripts")
def trigger_fetch_youtube_transcripts():
    """Triggers YouTube transcript collection."""
    fetch_youtube_transcripts(VIDEO_IDS, output_file=TRANSCRIPTS_FILE)
    return {"status": "success", "details": f"Transcripts saved to {TRANSCRIPTS_FILE}"}

# Generate Labeled Data Endpoint
@app.post("/generate_labeled_data")
def trigger_generate_labeled_data():
    """Triggers labeled Q/A data generation."""
    generate_labeled_data(input_file=TRANSCRIPTS_FILE, output_file=LABELED_DATA_FILE)
    return {"status": "success", "details": f"Labeled data saved to {LABELED_DATA_FILE}"}

# Fine-Tuning Endpoint
@app.post("/run_finetuning")
def trigger_finetuning():
    """Triggers the Fine-Tuning process."""
    train_dataset = LabeledDataset(data_file=LABELED_DATA_FILE)
    eval_dataset = LabeledDataset(data_file=LABELED_DATA_FILE)  # Placeholder for evaluation
    train_model(train_dataset, eval_dataset, CONFIG)
    return {"status": "success", "details": f"Model fine-tuned and saved to {CONFIG['output_dir']}"}

# Upload Model to Hugging Face Hub Endpoint
@app.post("/upload_model_to_hub")
def trigger_model_upload():
    """Triggers uploading the trained model to Hugging Face Hub."""
    repo_name = "ChaosKingNV/finetuned-ros2-model"  # Replace with your repository name
    upload_model_to_hub(repo_name=repo_name)
    return {"status": "success", "details": f"Model uploaded to Hugging Face Hub at {repo_name}"}

# Register Model with ClearML Endpoint
@app.post("/register_model_clearml")
def trigger_register_clearml():
    """Registers the fine-tuned model in ClearML."""
    register_model_with_clearml()
    return {"status": "success", "details": "Model registered in ClearML"}

# System Check Endpoint
@app.get("/system_check")
def system_check():
    """Runs system checks for the application."""

    checks = {
        "huggingface_model": "❌ Failed",
        "qdrant_connection": "❌ Failed",
        "fastapi_running": "❌ Failed",
        "gradio_running": "❌ Failed"
    }

    # Check Hugging Face Model
    try:
        from transformers import pipeline
        pipeline("text2text-generation", model="./local_model")
        checks["huggingface_model"] = "✅ Passed"
    except Exception as e:
        checks["huggingface_model"] = f"❌ Failed: {e}"

    # Check Qdrant Connection
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(url="http://qdrant:6333")
        collections = client.get_collections().collections
        if collections:
            checks["qdrant_connection"] = f"✅ Passed ({len(collections)} collections)"
        else:
            checks["qdrant_connection"] = "❌ No collections found in Qdrant."
    except Exception as e:
        checks["qdrant_connection"] = f"❌ Failed: {e}"

    # Check FastAPI
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            checks["fastapi_running"] = "✅ Passed"
        else:
            checks["fastapi_running"] = f"❌ Status: {response.status_code}"
    except Exception as e:
        checks["fastapi_running"] = f"❌ Not Reachable: {e}"

    # Check Gradio
    try:
        response = requests.get("http://localhost:7860/")
        if response.status_code == 200:
            checks["gradio_running"] = "✅ Passed"
        else:
            checks["gradio_running"] = f"❌ Status: {response.status_code}"
    except Exception as e:
        checks["gradio_running"] = f"❌ Not Reachable: {e}"

    return {"status": "completed", "checks": checks}

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
