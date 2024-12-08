import os
from pymongo import MongoClient

def clear_collection(collection_name):
    """
    Deletes all documents from the specified MongoDB collection.
    """
    # Get the MongoDB URI from the environment
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/")

    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client['rag_system']
        collection = db[collection_name]

        # Clear the collection
        result = collection.delete_many({})
        print(f"✅ Cleared {result.deleted_count} documents from collection '{collection_name}'.")

    except Exception as e:
        print(f"❌ Error clearing collection '{collection_name}': {e}")

    finally:
        client.close()
