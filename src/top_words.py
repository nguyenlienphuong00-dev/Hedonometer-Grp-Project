import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# -----------------------
# Load datasets
# -----------------------

df = pd.read_csv("data/processed/imdb_reviews_scored.csv")
labmt = pd.read_csv("data/processed/Data_Set_S1.csv")

labmt_dict = dict(zip(labmt["word"], labmt["happiness_average"]))

# -----------------------
# Tokenization
# -----------------------

def tokenize(text):
    text = str(text).lower()
    return re.findall(r"[a-z']+", text)

# -----------------------
# Stopwords
# -----------------------

stopwords = {
    "the","and","is","was","to","a","of","it","in","that",
    "this","for","with","as","on","but","not","you","are",
    "his","her","they","he","she","at","by","an","be","from",
    "or","we","my","so","if","about","what","which","who",
    "me","your","their","there","been","has","had","do","does",
    "have","one","all","just","out","it's","some"
}

# -----------------------
# EXTRA filter (important fix)
# -----------------------

exclude = {
    "movie","film","like","more","very","see","will",
    "one","people","first","most","well","story"
}

# -----------------------
# Collect words
# -----------------------

all_words = []

for review in df["review"]:
    tokens = tokenize(review)

    tokens = [
        w for w in tokens
        if w not in stopwords
        and w not in exclude
        and len(w) > 2
        and w in labmt_dict
        and (labmt_dict[w] <= 4 or labmt_dict[w] >= 6)
    ]

    all_words.extend(tokens)

# -----------------------
# Count frequencies
# -----------------------

word_counts = Counter(all_words)
top_words = word_counts.most_common(30)

words = [w for w, c in top_words]
counts = [c for w, c in top_words]

# -----------------------
# Plot (clean horizontal)
# -----------------------

plt.figure(figsize=(10, 8))
plt.barh(words, counts)

plt.title("Top Emotional Words in IMDb Reviews")
plt.xlabel("Frequency")
plt.ylabel("Words")

plt.tight_layout()
plt.savefig("figures/top_emotional_words.png")
plt.show()

print("DONE — check figures/top_emotional_words.png")