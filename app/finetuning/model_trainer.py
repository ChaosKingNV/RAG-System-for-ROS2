import torch
from transformers import BartForConditionalGeneration, AdamW
from transformers import get_scheduler
from torch.utils.data import DataLoader
from tqdm import tqdm

def train_model(train_dataset, eval_dataset, config):
    device = torch.device("cuda" if config["use_cuda"] and torch.cuda.is_available() else "cpu")
    print(f"🔧 Using device: {device}")

    model = BartForConditionalGeneration.from_pretrained(config["model_name"])
    model.to(device)

    train_loader = DataLoader(train_dataset, batch_size=config["train_batch_size"], shuffle=True)
    eval_loader = DataLoader(eval_dataset, batch_size=config["eval_batch_size"])

    optimizer = AdamW(model.parameters(), lr=config["learning_rate"])
    num_training_steps = len(train_loader) * config["num_train_epochs"]

    scheduler = get_scheduler(
        "linear", optimizer=optimizer, num_warmup_steps=config["warmup_steps"], num_training_steps=num_training_steps
    )

    model.train()
    for epoch in range(config["num_train_epochs"]):
        print(f"📚 Training Epoch {epoch + 1}")
        loop = tqdm(train_loader, leave=True)

        for batch in loop:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids, 
                attention_mask=attention_mask, 
                labels=input_ids  # Auto-regressive behavior
            )
            loss = outputs.loss

            loss.backward()
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

            loop.set_description(f"Epoch {epoch + 1}")
            loop.set_postfix(loss=loss.item())

    model.save_pretrained(config["output_dir"])
    print(f"✅ Model saved to {config['output_dir']}")
