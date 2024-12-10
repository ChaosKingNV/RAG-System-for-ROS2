from clearml import Task, InputModel

def register_model_with_clearml():
    """Register the Hugging Face model with ClearML and link its weights."""

    huggingface_model_name = "ChaosKingNV/finetuned-ros2-model"
    weights_url = f"https://huggingface.co/ChaosKingNV/finetuned-ros2-model/resolve/main/model.safetensors"

    print("🔗 Registering model in ClearML...")

    try:
        # Initialize ClearML task
        task = Task.init(
            project_name="RAG-Finetuning-Project",
            task_name="Model Registration",
            task_type="inference"
        )

        # Import the Hugging Face model as a ClearML input model
        registered_model = InputModel.import_model(
            name="ROS2 Finetuned Model",
            weights_url=weights_url,
            framework="Transformers",
            tags=["fine-tuned", "huggingface", "ros2"]
        )

        print("✅ Model successfully registered in ClearML.")
        print(f"🆔 ClearML Model ID: {registered_model.id}")
    except Exception as e:
        print(f"❌ Error registering model in ClearML: {e}")
