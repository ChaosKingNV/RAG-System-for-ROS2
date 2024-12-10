from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import ETL and Featurization Pipelines
from etl.etl_pipeline import run_etl_pipeline
from featurization.featurization_pipeline import run_featurization_pipeline

# Import YouTube Data Pipelines
from youtube_pipeline.youtube_transcript_collector import fetch_youtube_transcripts
from youtube_pipeline.question_answer_generator import generate_labeled_data
from youtube_pipeline.config import VIDEO_IDS, TRANSCRIPTS_FILE, LABELED_DATA_FILE

# Initialize FastAPI
app = FastAPI(
    title="AI Project API",
    description="API for ETL, Featurization, and YouTube Labeling Pipelines",
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

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
