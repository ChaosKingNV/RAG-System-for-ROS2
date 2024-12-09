from fastapi import FastAPI
from etl.etl_pipeline import run_etl_pipeline

# Initialize FastAPI
app = FastAPI()

@app.post("/run_etl")
def trigger_etl():
    """Triggers the ETL pipeline from a single function."""
    return run_etl_pipeline()


# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
