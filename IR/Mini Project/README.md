# Tweet Sentiment Analysis — Machine Learning Mini-Project

A beginner-friendly project that trains a model on labeled tweets and predicts **positive**, **neutral**, or **negative** sentiment.

## Dataset
Download the Twitter US Airline Sentiment dataset from Kaggle:
https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment

Extract the archive and place `Tweets.csv` in this project folder. The program uses the `text` and `airline_sentiment` columns.

## Install
Python 3.9+ recommended.

```bash
pip install -r requirements.txt
```

## 1. Train and evaluate
```bash
python train_model.py
```
This cleans the data, creates a stratified 80/20 train-test split, converts text using TF-IDF, trains Logistic Regression, prints accuracy and a classification report, and saves the trained model and evaluation files.

## 2. Run the prediction app
```bash
streamlit run app.py
```
Enter a tweet in the browser and click **Predict sentiment**.

## Files
- `train_model.py` — preprocessing, training, evaluation
- `app.py` — Streamlit prediction interface
- `requirements.txt` — dependencies
- `Tweets.csv` — download separately from Kaggle
- `sentiment_model.joblib` — generated trained model
- `evaluation_report.txt` and `metrics.json` — generated results

## Model
- TF-IDF features (unigrams and bigrams)
- Logistic Regression classifier
- Three classes: negative, neutral, positive
- Evaluation on a held-out test set; actual metrics print during training

## Limitations
The dataset concerns US airline feedback from 2015. Predictions may be less reliable for other topics, sarcasm, new slang, or other languages. Model scores are estimates, not guarantees.
