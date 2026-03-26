import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# -----------------------
# Make sure figures folder exists
# -----------------------
os.makedirs("figures", exist_ok=True)

# -----------------------
# Load data
# -----------------------
df = pd.read_csv("data/processed/imdb_reviews_scored.csv")

# -----------------------
# Tokenization
# -----------------------
def tokenize(text):
    text = str(text).lower()
    return re.findall(r"[a-z']+", text)

# -----------------------
# Stopwords (keep it simple for now)
# -----------------------
stopwords = {
    "the","and","is","was","to","a","of","it","in","that",
    "this","for","with","as","on","but","not","you","are",
    "his","her","they","he","she","at","by","an","be","from",
    "or","we","my","so","if","about","what","which","who",
    "me","your","their","there","been","has","had","do","does"
}

# -----------------------
# Create suspicious datasets
# -----------------------
pos_mean = df[df["sentiment"] == "pos"]["happiness_score"].mean()
neg_mean = df[df["sentiment"] == "neg"]["happiness_score"].mean()

suspicious_neg = df[
    (df["sentiment"] == "neg") &
    (df["happiness_score"] > pos_mean)
]

suspicious_pos = df[
    (df["sentiment"] == "pos") &
    (df["happiness_score"] < neg_mean)
]

print("Suspicious negative:", len(suspicious_neg))
print("Suspicious positive:", len(suspicious_pos))

# -----------------------
# Function to get top words (LESS STRICT)
# -----------------------
def get_top_words(dataframe):
    all_words = []

    for review in dataframe["review"]:
        tokens = tokenize(review)

        # only basic cleaning (NOT too strict)
        tokens = [
            w for w in tokens
            if w not in stopwords
            and len(w) > 2
        ]

        all_words.extend(tokens)

    counts = Counter(all_words)
    return counts.most_common(15)

# -----------------------
# Get top words
# -----------------------
top_neg = get_top_words(suspicious_neg)
top_pos = get_top_words(suspicious_pos)

print("Top negative words:", top_neg)
print("Top positive words:", top_pos)

# -----------------------
# Plot function
# -----------------------
def plot_words(word_list, title, filename):
    if not word_list:
        print(f"No data for {title}")
        return

    words = [w for w, c in word_list]
    counts = [c for w, c in word_list]

    plt.figure(figsize=(10, 8))
    plt.barh(words, counts)

    plt.title(title)
    plt.xlabel("Frequency")
    plt.ylabel("Words")

    plt.tight_layout()
    plt.savefig(filename)

    print(f"Saved: {filename}")

    plt.show()

# -----------------------
# Create plots
# -----------------------
plot_words(
    top_neg,
    "Top Words in Suspicious Negative Reviews",
    "figures/suspicious_negative_words.png"
)

plot_words(
    top_pos,
    "Top Words in Suspicious Positive Reviews",
    "figures/suspicious_positive_words.png"
)

print("DONE — check figures folder")