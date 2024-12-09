# app/featurization/vector_storer.py

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Initialize Qdrant client globally
qdrant_client = QdrantClient(url="http://qdrant:6333")

# Collection-specific ID counters
collection_point_counters = {}


def ensure_collection_exists(collection_name, vector_size=384):
    """
    Ensures the collection exists in Qdrant; creates it if it doesn't.
    """
    try:
        # Get list of all collections
        collections = qdrant_client.get_collections().collections

        # Check if the collection exists
        if not any(collection.name == collection_name for collection in collections):
            # Create the collection if it doesn't exist
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            # Initialize collection-specific counter
            collection_point_counters[collection_name] = 0
            print(f"✅ Created collection '{collection_name}' in Qdrant.")
        else:
            # If collection exists, sync counter
            collection_point_counters[collection_name] = (
                qdrant_client.get_collection(collection_name).points_count
            )
            print(f"✅ Collection '{collection_name}' already exists in Qdrant (starting from ID {collection_point_counters[collection_name]}).")
    except Exception as e:
        print(f"❌ Error ensuring collection '{collection_name}': {e}")


def store_embeddings_in_qdrant(embeddings, documents, collection_name):
    """
    Stores embeddings and corresponding metadata in Qdrant.
    """
    try:
        # Ensure collection exists
        ensure_collection_exists(collection_name, vector_size=len(embeddings[0]))

        # Get current collection-specific counter
        current_counter = collection_point_counters[collection_name]

        points = [
            PointStruct(
                id=current_counter + i,
                vector=embedding.tolist(),
                payload={"content": doc["content"], "url": doc["url"]}
            )
            for i, (embedding, doc) in enumerate(zip(embeddings, documents))
        ]

        # Increment the collection-specific counter
        collection_point_counters[collection_name] += len(points)

        # Upsert points into Qdrant
        qdrant_client.upsert(collection_name=collection_name, points=points)
        print(f"✅ Stored {len(points)} vectors in Qdrant for '{collection_name}' (Next ID: {collection_point_counters[collection_name]}).")

    except Exception as e:
        print(f"❌ Error storing vectors in Qdrant: {e}")
