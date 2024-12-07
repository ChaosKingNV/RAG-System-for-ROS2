import os
from pymongo import MongoClient

def store_data_in_mongo(data, collection_name):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Get MongoDB URI from environment variable
    try:
        client = MongoClient(MONGO_URI)
        db = client['rag_system']
        collection = db[collection_name]  # Select collection
        
        # Validate data
        if not isinstance(data, list):
            raise ValueError("Data should be a list of dictionaries.")

        collection.insert_many(data)  # Insert data into the collection
        print(f"✅ Data successfully inserted into collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error inserting data into MongoDB: {e}")
    finally:
        client.close()  # Close the MongoDB connection after operation
