from fastapi import FastAPI
from etl.github_fetcher import fetch_ros2_middleware_docs
from etl.mongodb_loader import store_data_in_mongo
from etl.clear_collection import clear_collection


app = FastAPI()

@app.post("/run_etl")
def trigger_etl():
    try:
        # Clear the old collection
        clear_collection("ros2_docs")
        
        # Fetch GitHub docs
        github_docs = fetch_ros2_middleware_docs()
        
        # Store docs in MongoDB
        store_data_in_mongo(github_docs, "ros2_docs")

        return {"message": f"✅ ETL pipeline executed successfully! {len(github_docs)} docs inserted."}
    except Exception as e:
        return {"message": f"❌ ETL pipeline failed: {e}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
