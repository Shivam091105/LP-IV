import os
import re
import joblib
import streamlit as st

MODEL_PATH = "sentiment_model.joblib"

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    return re.sub(r"\\s+", " ", text).strip()

st.set_page_config(page_title="Tweet Sentiment Analyzer", page_icon="💬")
st.title("Tweet Sentiment Analysis")
st.write("Enter a tweet and the trained model will predict its sentiment.")

if not os.path.exists(MODEL_PATH):
    st.error("Trained model not found. Run `python train_model.py` first.")
    st.stop()

model = joblib.load(MODEL_PATH)
tweet = st.text_area("Enter tweet text",
    placeholder="The flight was great and the staff were very helpful!")

if st.button("Predict sentiment", type="primary"):
    if not tweet.strip():
        st.warning("Please enter a tweet first.")
    else:
        prediction = model.predict([clean_text(tweet)])[0]
        probabilities = model.predict_proba([clean_text(tweet)])[0]
        confidence = max(probabilities) * 100

        if prediction == "positive":
            st.success(f"Predicted sentiment: {prediction.upper()}")
        elif prediction == "negative":
            st.error(f"Predicted sentiment: {prediction.upper()}")
        else:
            st.info(f"Predicted sentiment: {prediction.upper()}")

        st.write(f"Highest class score: {confidence:.1f}%")
        st.caption("This score is a model estimate, not a guarantee of correctness.")
        st.subheader("Scores by class")
        for label, score in sorted(zip(model.classes_, probabilities),
                                   key=lambda item: item[1], reverse=True):
            st.write(f"{label.title()}: {score * 100:.1f}%")
            st.progress(float(score))
