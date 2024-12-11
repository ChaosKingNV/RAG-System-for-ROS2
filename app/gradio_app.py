import gradio as gr
from transformers import pipeline

# Initialize the Hugging Face model pipeline
model = pipeline("text2text-generation", model="ChaosKingNV/finetuned-ros2-model")

# Define the prediction function
def answer_query(question):
    print(f"🔎 Received Query: {question}")  # Log received query
    result = model(question, max_length=256, num_beams=4, early_stopping=True)
    answer = result[0]["generated_text"]
    print(f"✅ Answer Generated: {answer}")  # Log generated answer
    return answer

# Create the Gradio interface
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
