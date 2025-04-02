from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load SBERT for deep context understanding
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load RoBERTa-based GoEmotions model
MODEL_NAME = "joeddav/distilbert-base-uncased-go-emotions-student"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Emotion labels from GoEmotions dataset
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval",
    "caring", "confusion", "curiosity", "desire", "disappointment",
    "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism",
    "pride", "realization", "relief", "remorse", "sadness", "surprise"
]

def detect_emotion(text):
    """Detects emotions in user input using SBERT + RoBERTa-GoEmotions"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    scores = outputs.logits.softmax(dim=1)
    
    # Get top 2 emotions (multi-label classification)
    top_indices = torch.topk(scores, 2).indices[0].tolist()
    detected_emotions = [emotion_labels[i] for i in top_indices]
    
    return detected_emotions  # Return detected emotions as a list

# Example usage
if __name__ == "__main__":
    text = "I feel so lonely and hopeless..."
    print(f"Detected emotions: {detect_emotion(text)}")