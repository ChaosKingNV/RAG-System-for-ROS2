from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from etl.etl_pipeline import run_etl_pipeline
from featurization.featurization_pipeline import run_featurization_pipeline

# Initialize FastAPI
app = FastAPI(
    title="AI Project API",
    description="API for ETL and Featurization Pipelines",
    version="1.0.0"
)

# Mount static files (for favicon and other assets if needed)
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

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
