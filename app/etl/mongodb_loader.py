import os
from pymongo import MongoClient


def store_data_in_mongo(data, collection_name):
    """
    Stores data in MongoDB collection.

    Args:
        data (list): List of documents to store in MongoDB.
        collection_name (str): Name of the MongoDB collection.
    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client['rag_system']
        collection = db[collection_name]

        # Validate and Insert Data
        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ No valid data to insert into '{collection_name}'.")
            return

        result = collection.insert_many(data)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} documents into collection '{collection_name}'.")

    except Exception as e:
        print(f"❌ Error inserting data into MongoDB: {e}")
    finally:
        client.close()  # Close MongoDB connection
