import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(
    'data/raw/Data_Set_S1.txt',
    sep='\t',
    skiprows=3,
    na_values='--'
)

# Count words present in each corpus (rank not missing)
corpora = {
    "Twitter": "twitter_rank",
    "Google Books": "google_rank",
    "NYT": "nyt_rank",
    "Lyrics": "lyrics_rank"
}

counts = {}

for name, column in corpora.items():
    counts[name] = df[column].notna().sum()

print("Word counts in top 5000 by corpus:")
for name, count in counts.items():
    print(f"{name}: {count}")

# Compute overlaps
twitter = set(df.loc[df["twitter_rank"].notna(), "word"])
google = set(df.loc[df["google_rank"].notna(), "word"])
nyt = set(df.loc[df["nyt_rank"].notna(), "word"])
lyrics = set(df.loc[df["lyrics_rank"].notna(), "word"])

print("\nOverlap Twitter & NYT:", len(twitter & nyt))
print("Overlap in all four:", len(twitter & google & nyt & lyrics))

# Example word: present in Twitter but not Google Books
example = list(twitter - google)
if example:
    print("Example word in Twitter but not Google Books:", example[0])

# Plot bar chart
plt.bar(counts.keys(), counts.values())
plt.title("Number of labMT Words in Top 5000 by Corpus")
plt.ylabel("Number of Words")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figures/corpus_counts.png")
plt.show()