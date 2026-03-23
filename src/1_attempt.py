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

# load scored IMDb dataset
df = pd.read_csv("data/processed/imdb_reviews_scored.csv")

print("Columns:", df.columns)

# -------- GRAPH 1 (you already have) --------
# small dataset barplot

small_df = df.sample(n=100, random_state=42)

# save it
small_df.to_csv("data/processed/imdb_small.csv", index=False)

print("\nSmall dataset created:", len(small_df))

# compare means
print("\nMean comparison:")
print("Full:", df["happiness_score"].mean())
print("Small:", small_df["happiness_score"].mean())

# compare positive vs negative
print("\nBy label:")
print(small_df.groupby("sentiment")["happiness_score"].mean())

import matplotlib.pyplot as plt

# calculate means by sentiment
means = small_df.groupby("sentiment")["happiness_score"].mean()

# plot
means.plot(kind="bar")

plt.title("Average Happiness Score by Review Sentiment (Small Dataset)")
plt.xlabel("Sentiment")
plt.ylabel("Average Happiness Score")

plt.tight_layout()
plt.savefig("figures/smaller_dataset_barplot.png")
plt.show()

#-----
small_df = df.sample(n=1000, random_state=42)

# save it
small_df.to_csv("data/processed/imdb_small.csv", index=False)

print("\nSmall dataset created:", len(small_df))

# compare means
print("\nMean comparison:")
print("Full:", df["happiness_score"].mean())
print("Small:", small_df["happiness_score"].mean())

# compare positive vs negative
print("\nBy label:")
print(small_df.groupby("sentiment")["happiness_score"].mean())

import matplotlib.pyplot as plt

# calculate means by sentiment
means = small_df.groupby("sentiment")["happiness_score"].mean()

# plot
means.plot(kind="bar")

plt.title("Average Happiness Score by Review Sentiment (Small Dataset)")
plt.xlabel("Sentiment")
plt.ylabel("Average Happiness Score")

plt.tight_layout()
plt.savefig("figures/small_dataset_barplot.png")
plt.show()

# -------- GRAPH 2 --------
# FULL vs SMALL comparison plot
full_means = df.groupby("sentiment")["happiness_score"].mean()
small_means = small_df.groupby("sentiment")["happiness_score"].mean()

import pandas as pd
comparison = pd.DataFrame({
    "Full Dataset": full_means,
    "Small Dataset": small_means
})

comparison.plot(kind="bar")

plt.title("Full vs Small Dataset: Happiness Scores by Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Average Happiness Score")

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("figures/full_vs_small_comparison.png")
# plt.show()