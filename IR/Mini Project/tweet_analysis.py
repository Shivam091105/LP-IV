
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

# Download VADER sentiment dictionary
nltk.download("vader_lexicon", quiet=True)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

tweets = []
sentiments = []

print("===== TWEET SENTIMENT ANALYSIS SYSTEM =====")
print("Enter tweets one by one.")
print("Type 'exit' to finish analysis.\n")

while True:
    tweet = input("Enter a tweet: ").strip()

    if tweet.lower() == "exit":
        break

    if not tweet:
        print("Please enter a non-empty tweet.")
        continue

    # Calculate sentiment scores
    scores = analyzer.polarity_scores(tweet)
    compound = scores["compound"]

    # Classify sentiment
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    tweets.append(tweet)
    sentiments.append(sentiment)

    print("Sentiment:", sentiment)
    print("Compound score:", round(compound, 3), "\n")

# Display summary report
print("\n===== SENTIMENT ANALYSIS REPORT =====")

if not tweets:
    print("No tweets were entered.")
else:
    counts = Counter(sentiments)

    print("Total tweets:", len(tweets))
    print("Positive tweets:", counts["Positive"])
    print("Negative tweets:", counts["Negative"])
    print("Neutral tweets:", counts["Neutral"])

    print("\n----- Detailed Results -----")
    for tweet, sentiment in zip(tweets, sentiments):
        print(f"{sentiment}: {tweet}")
