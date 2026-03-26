import pandas as pd

df = pd.read_csv("data/raw/Data_Set_S1.txt",
                 delimiter="\t",
                 skiprows=3,
                 na_values=["--"]
)

df.to_csv("data/processed/Data_Set_S1.csv", index=False) # index=False doesnt save row numbers as the first column - would move all columns to the right?

df = pd.read_csv("data/processed/Data_Set_S1.csv")

print(df.columns)

print(df.dtypes)
print(df.info()) #or RangeIndex indicates rows, to confirm print(len(df)) is also possible
#print(df.describe())
print(df.isna().sum()) #gives what how many cells are empty

duplicates=df.duplicated(subset=["word"], keep=False) #looks at the word column, marking all duplicates as true
print(duplicates)
print(df[["word", "happiness_average"]].head(10))
#double brackets when selecting multiple columns, returning a dataframe
print(df[["word", "happiness_average"]].tail(10))

import numpy as np
import re

# load labMT dictionary
labmt_dict = dict(zip(df["word"], df["happiness_average"]))


# tokenize function
def tokenize(text):

    if pd.isna(text):
        return []

    text = text.lower()

    return re.findall(r"[a-z']+", text)


# hedonometer score
def hedonometer_score(text):

    tokens = tokenize(text)

    scores = []

    for w in tokens:

        if w in labmt_dict:

            s = labmt_dict[w]

            if s <= 4 or s >= 6:
                scores.append(s)

    if len(scores) == 0:
        return None

    return np.mean(scores)


# apply score
if "text" in df.columns:
    df["happiness_score"] = df["text"].apply(hedonometer_score)
    df.to_csv("../data/processed/Data_Set_S1_scored.csv", index=False)

    print("\nHappiness scores calculated and saved.")
else:
    print("\nNo 'text' column found — hedonometer scoring skipped.")

#Apply hedonometer scoring to IMDb corpus

corpus = pd.read_csv("data/raw/imdb_reviews.csv")

print("Corpus columns:", corpus.columns)

# compute happiness score for each review
corpus["happiness_score"] = corpus["review"].apply(hedonometer_score)

# save scored corpus
corpus.to_csv("data/processed/imdb_reviews_scored.csv", index=False)

print("Hedonometer scoring completed.")

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# load FULL dataset
df = pd.read_csv("data/processed/imdb_reviews_scored.csv")

def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-z']+", text)

stopwords = {"the", "and", "is", "was", "to", "a", "of", "it", "in", "that"}

all_words = []

for review in df["review"]:
    tokens = tokenize(review)
    tokens = [w for w in tokens if w not in stopwords and len(w) > 2]
    all_words.extend(tokens)

word_counts = Counter(all_words)

top_words = word_counts.most_common(10)

words = [w for w, c in top_words]
counts = [c for w, c in top_words]

plt.bar(words, counts)

plt.title("Top 10 Most Frequent Words (IMDb Dataset)")
plt.xlabel("Words")
plt.ylabel("Frequency")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("figures/top_words_barplot.png")