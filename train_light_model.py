from datasets import load_dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch


def main():
    # -------------------------------
    # 🔥 CHECK GPU
    # -------------------------------
    print("GPU Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU Name:", torch.cuda.get_device_name(0))

    # -------------------------------
    # STEP 1: Load dataset
    # -------------------------------
    ds = load_dataset("guychuk/benign-malicious-prompt-classification")

    # Split dataset
    ds = ds["train"].train_test_split(test_size=0.2)

    print("✅ Dataset loaded")

    # 🔥 FAST MODE
    ds["train"] = ds["train"].shuffle(seed=42).select(range(30000))
    ds["test"] = ds["test"].shuffle(seed=42).select(range(5000))

    # -------------------------------
    # STEP 2: Tokenizer
    # -------------------------------
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

    def tokenize(batch):
        return tokenizer(
            batch["prompt"],
            padding="max_length",
            truncation=True,
            max_length=128
        )

    ds = ds.map(tokenize, batched=True)

    # Rename label column
    ds = ds.rename_column("label", "labels")

    # Ensure labels are integers
    ds = ds.map(lambda x: {"labels": int(x["labels"])})

    # Keep only required columns
    ds = ds.remove_columns(
        [col for col in ds["train"].column_names if col not in ["input_ids", "attention_mask", "labels"]]
    )

    ds.set_format("torch")

    print("✅ Tokenization complete")

    # -------------------------------
    # STEP 3: Model
    # -------------------------------
    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=2
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # -------------------------------
    # STEP 4: Metrics
    # -------------------------------
    def compute_metrics(pred):
        labels = pred.label_ids
        preds = np.argmax(pred.predictions, axis=1)

        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, preds, average='binary'
        )
        acc = accuracy_score(labels, preds)

        return {
            "accuracy": acc,
            "f1": f1,
            "precision": precision,
            "recall": recall
        }

    # -------------------------------
    # STEP 5: Training Config
    # -------------------------------
    training_args = TrainingArguments(
        output_dir="./models/distilbert",

        learning_rate=3e-5,

        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,

        gradient_accumulation_steps=4,

        num_train_epochs=2,

        weight_decay=0.01,

        fp16=torch.cuda.is_available(),

        logging_steps=200,

        dataloader_num_workers=0  # 🔥 FIXED (NO CRASH)
    )

    # -------------------------------
    # STEP 6: Trainer
    # -------------------------------
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds["train"],
        eval_dataset=ds["test"],
        compute_metrics=compute_metrics
    )

    # -------------------------------
    # STEP 7: Train
    # -------------------------------
    print("🚀 Training started...")
    trainer.train()

    # -------------------------------
    # STEP 8: Evaluate
    # -------------------------------
    results = trainer.evaluate()
    print("📊 Final Results:", results)

    # -------------------------------
    # STEP 9: Save model
    # -------------------------------
    trainer.save_model("models/distilbert")
    tokenizer.save_pretrained("models/distilbert")

    print("✅ Model trained & saved successfully!")


# 🔥 VERY IMPORTANT FOR WINDOWS
if __name__ == "__main__":
    main()