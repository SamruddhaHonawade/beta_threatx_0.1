from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

# Load trained model
tokenizer = DistilBertTokenizerFast.from_pretrained("models/distilbert")
model = DistilBertForSequenceClassification.from_pretrained("models/distilbert")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def check_ml(text: str) -> float:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)
    malicious_prob = probs[0][1].item()

    print("ML SCORE:", malicious_prob)  # debug

    return round(malicious_prob, 3)