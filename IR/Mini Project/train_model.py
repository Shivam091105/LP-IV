import re
import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATASET_PATH = "Tweets.csv"
MODEL_PATH = "sentiment_model.joblib"

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    return re.sub(r"\\s+", " ", text).strip()

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    required = {"text", "airline_sentiment"}
    if not required.issubset(df.columns):
        raise ValueError(f"Tweets.csv must contain columns: {required}")

    df = df[["text", "airline_sentiment"]].dropna()
    df["text"] = df["text"].apply(clean_text)
    df = df[df["text"].str.len() > 0].drop_duplicates(subset=["text"])
    X = df["text"]
    y = df["airline_sentiment"].str.lower()

    print(f"Usable tweets: {len(df)}")
    print("\nClass distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1, 2),
                                  stop_words="english")),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    print("\nTraining model...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, zero_division=0)
    matrix = confusion_matrix(y_test, predictions,
                              labels=["negative", "neutral", "positive"])

    print(f"\nTest accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)")
    print("\nClassification report:")
    print(report)
    print("Confusion matrix (negative, neutral, positive):")
    print(matrix)

    joblib.dump(model, MODEL_PATH)
    with open("evaluation_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Test accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n\n")
        f.write(report)
        f.write("\nConfusion matrix (negative, neutral, positive):\n")
        f.write(str(matrix))
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump({"dataset_rows_used": int(len(df)),
                   "train_rows": int(len(X_train)),
                   "test_rows": int(len(X_test)),
                   "test_accuracy": float(accuracy),
                   "classes": ["negative", "neutral", "positive"]}, f, indent=2)
    print(f"\nSaved model to {MODEL_PATH}")
    print("Saved evaluation_report.txt and metrics.json")

if __name__ == "__main__":
    main()
