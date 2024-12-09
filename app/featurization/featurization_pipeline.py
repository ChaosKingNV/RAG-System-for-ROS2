# app/featurization/featurization_pipeline.py

from featurization.mongo_reader import fetch_and_clean_documents_in_batches
from featurization.featurizer import generate_embeddings
from featurization.vector_storer import store_embeddings_in_qdrant
from tqdm import tqdm

# Batch size configuration
BATCH_SIZE = 500  

def run_featurization_pipeline():
    """
    Executes the featurization pipeline by processing documents in batches.
    """
    try:
        collections_to_process = ["ros2_docs", "nav2_docs", "moveit2_docs", "gazebo_docs"]
        total_processed = 0

        for collection_name in collections_to_process:
            print(f"🚀 Starting featurization for '{collection_name}'...")

            for batch_documents in fetch_and_clean_documents_in_batches(collection_name, BATCH_SIZE):
                if not batch_documents:
                    print(f"⚠️ No more documents in '{collection_name}'. Skipping...")
                    break

                # Generate embeddings
                embeddings = generate_embeddings([doc["content"] for doc in batch_documents])

                # Store embeddings in Qdrant
                store_embeddings_in_qdrant(embeddings, batch_documents, collection_name)

                total_processed += len(batch_documents)
                print(f"✅ Processed batch of {len(batch_documents)} from '{collection_name}'.")

            print(f"✅ Completed featurization for '{collection_name}'.")

        return {"message": f"✅ Featurization completed! Total processed: {total_processed}"}

    except Exception as e:
        print(f"❌ Featurization pipeline failed: {e}")
        return {"message": f"❌ Featurization pipeline failed: {e}"}
