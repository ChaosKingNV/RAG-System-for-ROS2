from pymongo import MongoClient

def store_data_in_mongo(data, collection_name):
    client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
    db = client['rag_system']
    collection = db[collection_name]  # Select collection (like a folder)
    collection.insert_many(data)  # Insert data into the collection
