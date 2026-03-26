from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

REVIEWS_PATH = Path("data/raw/imdb_reviews.csv")
LEXICON_PATH = Path("data/raw/Data_Set_S1.txt")
FIGURES_DIR = Path("figures")
PROCESSED_PATH = Path("data/processed/imdb_reviews_with_scores.csv")


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


def make_wordcloud(text, output_path, title, stopwords):
    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        stopwords=stopwords,
        collocations=False
    ).generate(text)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(REVIEWS_PATH)

    required_cols = {"sentiment", "review"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in imdb_reviews.csv: {missing}")

    lexicon = load_lexicon(LEXICON_PATH)

    df["happiness"] = df["review"].apply(lambda x: review_score(x, lexicon))
    df = df.dropna(subset=["happiness"]).copy()

    pos_mean = df[df["sentiment"] == "pos"]["happiness"].mean()
    neg_mean = df[df["sentiment"] == "neg"]["happiness"].mean()

    print("Positive mean:", pos_mean)
    print("Negative mean:", neg_mean)

    suspicious_neg = df[(df["sentiment"] == "neg") & (df["happiness"] > pos_mean)].copy()
    suspicious_pos = df[(df["sentiment"] == "pos") & (df["happiness"] < neg_mean)].copy()

    print("Suspicious negative:", len(suspicious_neg))
    print("Suspicious positive:", len(suspicious_pos))

    print("\nSample suspicious negative reviews:")
    print(suspicious_neg[["sentiment", "happiness", "review"]].head(5))

    print("\nSample suspicious positive reviews:")
    print(suspicious_pos[["sentiment", "happiness", "review"]].head(5))

    sample_size_neg = min(1000, len(suspicious_neg))
    sample_size_pos = min(1000, len(suspicious_pos))

    suspicious_neg_sample = suspicious_neg.sample(n=sample_size_neg, random_state=42) if sample_size_neg > 0 else suspicious_neg
    suspicious_pos_sample = suspicious_pos.sample(n=sample_size_pos, random_state=42) if sample_size_pos > 0 else suspicious_pos

    print("\nSampled suspicious negative reviews:", len(suspicious_neg_sample))
    print("Sampled suspicious positive reviews:", len(suspicious_pos_sample))

    stopwords = set(STOPWORDS)
    stopwords.update([
        "movie", "film", "one", "really", "would", "could", "also",
        "get", "got", "made", "make", "much", "even"
    ])

    if len(suspicious_neg_sample) > 0:
        neg_text = " ".join(suspicious_neg_sample["review"].astype(str))
        make_wordcloud(
            neg_text,
            FIGURES_DIR / "suspicious_negative_wordcloud.png",
            "Suspicious Negative Reviews (Random Sample of 1000)",
            stopwords
        )
    else:
        print("No suspicious negative reviews found.")

    if len(suspicious_pos_sample) > 0:
        pos_text = " ".join(suspicious_pos_sample["review"].astype(str))
        make_wordcloud(
            pos_text,
            FIGURES_DIR / "suspicious_positive_wordcloud.png",
            "Suspicious Positive Reviews (Random Sample of 1000)",
            stopwords
        )
    else:
        print("No suspicious positive reviews found.")

    df.to_csv(PROCESSED_PATH, index=False)

    print("\nSaved:")
    print(PROCESSED_PATH)
    print(FIGURES_DIR / "suspicious_negative_wordcloud.png")
    print(FIGURES_DIR / "suspicious_positive_wordcloud.png")


if __name__ == "__main__":
    main()
    