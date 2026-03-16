
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



df = pd.read_csv('data/processed/imdb_reviews_scored.csv')
print(df.columns)

#1. BOXPLOT: Hedonometer Scores across IMDb Sentiment Labels
plt.figure(figsize=(8, 6)) 
sns.boxplot(data=df, x='sentiment', y='happiness_score', palette='Set2')


plt.title('Hedonometer Scores across IMDb Sentiment Labels', fontsize=14)
plt.xlabel('Actual IMDb Sentiment', fontsize=12)
plt.ylabel('Hedonometer Happiness Score', fontsize=12)


plt.savefig('figures/boxplot_accuracy.png', bbox_inches='tight')
plt.show()

