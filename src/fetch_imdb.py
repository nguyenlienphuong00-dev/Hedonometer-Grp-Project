from pathlib import Path
import pandas as pd

IMDB_PATH = Path("/Users/seoyeonkim/Downloads/aclImdb")
OUTPUT_PATH = Path("data/processed/imdb_reviews.csv")


def load_reviews(base_path: Path) -> pd.DataFrame:
    rows = []

    for split in ["train", "test"]:
        for sentiment in ["pos", "neg"]:
            folder = base_path / split / sentiment

            for txt_file in folder.glob("*.txt"):
                text = txt_file.read_text(encoding="utf-8")
                rows.append({
                    "split": split,
                    "sentiment": sentiment,
                    "review": text
                })

    df = pd.DataFrame(rows)
    return df


def main():
    print("STARTING IMDB LOADING...")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_reviews(IMDB_PATH)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Saved", len(df), "reviews")
    print("Output file:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
    