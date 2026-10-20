# Data Preprocessing and Similarity Calculation using TF-IDF and Cosine Similarity

import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLP resources
for resource in [
    "stopwords", "punkt", "punkt_tab", "wordnet",
    "omw-1.4", "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng"
]:
    nltk.download(resource, quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# Convert POS tags into WordNet format
def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return "a"  # Adjective
    elif tag.startswith("V"):
        return "v"  # Verb
    elif tag.startswith("N"):
        return "n"  # Noun
    elif tag.startswith("R"):
        return "r"  # Adverb
    return "n"


# Preprocess a document
def preprocess(text):
    tokens = word_tokenize(text.lower())

    # Remove punctuation and stop words
    tokens = [
        word for word in tokens
        if word not in string.punctuation
        and word not in stop_words
        and any(char.isalnum() for char in word)
    ]

    # POS tagging and lemmatization
    tagged_words = pos_tag(tokens)

    processed_words = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        for word, tag in tagged_words
    ]

    return " ".join(processed_words)


# Input two documents
doc1 = input("Enter the first document: ")
doc2 = input("Enter the second document: ")

# Preprocess documents
clean_doc1 = preprocess(doc1)
clean_doc2 = preprocess(doc2)

print("\nPreprocessed Document 1:", clean_doc1)
print("Preprocessed Document 2:", clean_doc2)

# Convert documents into TF-IDF vectors
vectorizer = TfidfVectorizer()

try:
    tfidf_matrix = vectorizer.fit_transform([clean_doc1, clean_doc2])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:2]
    )[0][0]

    print(f"\nCosine Similarity: {similarity:.4f}")
    print(f"Similarity Percentage: {similarity * 100:.2f}%")

except ValueError:
    print("\nSimilarity cannot be calculated because no words remain.")
