# app/featurization/featurizer.py

from sentence_transformers import SentenceTransformer

# Load the model globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embeddings(texts):
    """
    Generate embeddings for a list of texts using SentenceTransformer.
    """
    try:
        embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)
        print(f"✅ Generated {len(embeddings)} embeddings.")
        return embeddings
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return []
