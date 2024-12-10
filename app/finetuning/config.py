# Training Configurations
CONFIG = {
    "model_name": "facebook/bart-large",  # Use BART
    "train_batch_size": 8,    # Larger models need smaller batches
    "eval_batch_size": 4,
    "learning_rate": 3e-5,
    "num_train_epochs": 4,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "logging_steps": 10,
    "save_steps": 100,
    "output_dir": "finetuned_model",
    "use_cuda": True  # Enable CUDA if available
}
