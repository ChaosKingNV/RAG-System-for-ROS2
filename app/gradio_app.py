import gradio as gr
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Initialize models
text_generator = pipeline("text2text-generation", model="./local_model")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
qdrant_client = QdrantClient(url="http://qdrant:6333")

# List of collections to query
QDRANT_COLLECTIONS = ["nav2_docs", "moveit2_docs", "gazebo_docs", "ros2_docs"]


def smart_truncate_context(tokenizer, context, max_length=1024, question=""):
    """
    Intelligently truncate context while preserving relevant information.
    """
    encoded_context = tokenizer.encode(context, add_special_tokens=False)
    encoded_question = tokenizer.encode(question, add_special_tokens=False)

    # Ensure enough space for the question
    available_length = max_length - len(encoded_question)
    truncated_encoded = encoded_context[-available_length:]
    final_encoded = truncated_encoded + encoded_question

    # Decode back to text
    truncated_context = tokenizer.decode(final_encoded, skip_special_tokens=True)
    return truncated_context


def answer_query(question):
    try:
        print(f"🔎 Received Query: {question}")

        # Generate query embedding
        query_vector = embedder.encode(question).tolist()
        if len(query_vector) != 384:
            raise ValueError(f"Invalid query vector length: {len(query_vector)}")

        print(f"✅ Query Vector Generated: Length {len(query_vector)}")

        retrieved_docs = []

        # Search in each Qdrant collection
        for collection_name in QDRANT_COLLECTIONS:
            search_results = qdrant_client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=5
            )

            # Collect search results
            collection_docs = [hit.payload.get("content", "") for hit in search_results if "content" in hit.payload]
            retrieved_docs.extend(collection_docs)

        if not retrieved_docs:
            print("❌ No content retrieved from any collection.")
            return "❌ No relevant documents found in any collection."

        context = " ".join(retrieved_docs)
        print(f"✅ Retrieved Context (First 200 chars): {context[:200]}...")

        # Truncate the context
        context = smart_truncate_context(text_generator.tokenizer, context, max_length=1024, question=question)

        # Generate an answer using the text generation model
        result = text_generator(f"{context} Question: {question}", max_length=256, num_beams=4, early_stopping=True)

        if not result or not isinstance(result, list) or "generated_text" not in result[0]:
            print("❌ Unexpected response format from text generator.")
            return "❌ Unexpected response format. Please try again."

        answer = result[0]["generated_text"]
        print(f"✅ Answer Generated: {answer}")
        return answer

    except Exception as e:
        print(f"❌ Error during query processing: {e}")
        return f"❌ Something went wrong: {e}"


# Create the Gradio interface with an editable output text box
iface = gr.Interface(
    fn=answer_query, 
    inputs="text", 
    outputs="text", 
    title="RAG System for ROS2 Navigation",
    description="Ask specific questions related to ROS2, navigation, motion planning, and simulation."
)

if __name__ == "__main__":
    print("🚀 Starting Gradio Server... Listening on http://localhost:7860")
    iface.launch(server_name="0.0.0.0", server_port=7860)
