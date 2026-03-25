from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

REVIEWS_PATH = Path("data/raw/imdb_reviews.csv")
LEXICON_PATH = Path("data/raw/Data_Set_S1.txt")
FIGURES_DIR = Path("figures")

POS_MEAN = 6.12
NEG_MEAN = 5.75


def tokenize(text):
    return re.findall(r"\b[a-z']+\b", str(text).lower())


def load_lexicon(path):
    lex = pd.read_csv(path, sep=r"\s+", engine="python", skiprows=2)

    if "word" not in lex.columns:
        raise ValueError(f"Missing 'word' column. Found columns: {list(lex.columns)}")

    score_col = None
    for col in ["happiness_average", "happiness", "score"]:
        if col in lex.columns:
            score_col = col
            break

    if score_col is None:
        raise ValueError(
            f"No happiness score column found. Found columns: {list(lex.columns)}"
        )

    return dict(zip(lex["word"], lex[score_col]))


def review_score(text, lexicon):
    words = tokenize(text)
    scores = [lexicon[w] for w in words if w in lexicon]

    if not scores:
        return None

    return sum(scores) / len(scores)


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(REVIEWS_PATH)
    lexicon = load_lexicon(LEXICON_PATH)

    required_cols = {"sentiment", "review"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in imdb_reviews.csv: {missing}")

    df["happiness"] = df["review"].apply(lambda x: review_score(x, lexicon))
    df = df.dropna(subset=["happiness"]).copy()

    suspicious_neg = df[(df["sentiment"] == "neg") & (df["happiness"] > POS_MEAN)]
    suspicious_pos = df[(df["sentiment"] == "pos") & (df["happiness"] < NEG_MEAN)]

    print("Suspicious negative:", len(suspicious_neg))
    print("Suspicious positive:", len(suspicious_pos))

    neg_text = " ".join(suspicious_neg["review"].astype(str))
    pos_text = " ".join(suspicious_pos["review"].astype(str))

    stopwords = set(STOPWORDS)
    stopwords.update([
        "movie", "film", "one", "really", "would", "could", "also",
        "get", "got", "made", "make", "much", "even"
    ])

    if len(suspicious_neg) > 0:
        wc_neg = WordCloud(
            width=1200,
            height=600,
            background_color="white",
            stopwords=stopwords,
            collocations=False
        ).generate(neg_text)

        plt.figure(figsize=(12, 6))
        plt.imshow(wc_neg, interpolation="bilinear")
        plt.axis("off")
        plt.title("Suspicious Negative Reviews")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "suspicious_negative_wordcloud.png")
        plt.close()
    else:
        print("No suspicious negative reviews found.")

    if len(suspicious_pos) > 0:
        wc_pos = WordCloud(
            width=1200,
            height=600,
            background_color="white",
            stopwords=stopwords,
            collocations=False
        ).generate(pos_text)

        plt.figure(figsize=(12, 6))
        plt.imshow(wc_pos, interpolation="bilinear")
        plt.axis("off")
        plt.title("Suspicious Positive Reviews")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "suspicious_positive_wordcloud.png")
        plt.close()
    else:
        print("No suspicious positive reviews found.")

    df.to_csv("data/processed/imdb_reviews_with_scores.csv", index=False)

    print("Saved completed.")


if __name__ == "__main__":
    main()
    