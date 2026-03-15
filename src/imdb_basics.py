import numpy as np
import pandas as pd

df = pd.read_csv('data/processed/imdb_reviews.csv')

# Check what you have
print(df.head())
print(df.info())
print(df['sentiment'].value_counts())
print(df["split"].value_counts())