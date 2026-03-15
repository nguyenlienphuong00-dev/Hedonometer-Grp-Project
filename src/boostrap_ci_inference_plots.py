import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('data/processed/imdb_reviews_scored.csv')

#from now on gonna calculate sampled mean score of pos/neg reviews
positive = df[df['sentiment'] == 'pos']['happiness_score']
negative = df[df['sentiment'] == 'neg']['happiness_score']

n_bootstrap = 1000
pos_means = []
neg_means = []
diffs = []

for i in range(n_bootstrap):
    #resampling pos/neg seperately
    pos_boot = np.random.choice(positive, size=len(positive), replace=True)
    neg_boot = np.random.choice(negative, size=len(negative), replace=True)
    
    pos_means.append(np.mean(pos_boot))
    neg_means.append(np.mean(neg_boot))
    diffs.append(np.mean(pos_boot) - np.mean(neg_boot))

# Calculate confidence intervals
pos_ci = np.percentile(pos_means, [2.5, 97.5]) #cuz i want 95% confidence
neg_ci = np.percentile(neg_means, [2.5, 97.5])
diff_ci = np.percentile(diffs, [2.5, 97.5])

print(f"Positive mean: {np.mean(pos_means):.2f} (95% CI: [{pos_ci[0]:.2f}, {pos_ci[1]:.2f}])") #:.2f - 2 numbers after a . - formatting float
print(f"Negative mean: {np.mean(neg_means):.2f} (95% CI: [{neg_ci[0]:.2f}, {neg_ci[1]:.2f}])")
print(f"Difference: {np.mean(pos_means)-np.mean(neg_means):.2f} (95% CI: [{diff_ci[0]:.2f}, {diff_ci[1]:.2f}])")


bootstrap_positive_mean = np.mean(pos_means)

# NEGATIVE REVIEWS THAT SCORE HIGHLY IN HAPPINESS AND VICE VERSA - ACCURACY OF HEDONOMETER?
sus_neg_reviews = df[(df['sentiment'] == 'neg') & (df['happiness_score'] > bootstrap_positive_mean)]

print(f"\nFOUND {len(sus_neg_reviews)} NEGATIVE REVIEWS ABOVE THE BOOTSTRAP POSITIVE MEAN")
print(f"This is {len(sus_neg_reviews)/len(df[df['sentiment']=='neg'])*100:.1f}% of all negative reviews")

sus_pos_reviews = df[(df["sentiment"] == "pos") & (df["happiness_score"] < np.mean(neg_means))]
print(f"\nFOUND {len(sus_pos_reviews)} POSITIVE REVIEWS BELOW THE BOOSTRAP NEGATIVE MEAN")
print(f"This is {len(sus_pos_reviews)/len(df[df['sentiment']=='pos'])*100:.1f}% of all positive reviews")

# ///// INFERENCE PLOTS //////

#BOOSTRAP PLOT
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Positive distribution
axes[0].hist(pos_means, bins=30, color='green', alpha=0.7, edgecolor='black')
axes[0].axvline(np.mean(positive), color='darkgreen', linestyle='-', linewidth=2, label='Observed mean')
axes[0].axvline(pos_ci[0], color='red', linestyle='--', label='95% CI')
axes[0].axvline(pos_ci[1], color='red', linestyle='--')
axes[0].set_xlabel('Bootstrap Mean')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Positive Reviews\nBootstrap Distribution')
axes[0].legend()

# Negative distribution
axes[1].hist(neg_means, bins=30, color='red', alpha=0.7, edgecolor='black')
axes[1].axvline(np.mean(negative), color='darkred', linestyle='-', linewidth=2, label='Observed mean')
axes[1].axvline(neg_ci[0], color='blue', linestyle='--', label='95% CI')
axes[1].axvline(neg_ci[1], color='blue', linestyle='--')
axes[1].set_xlabel('Bootstrap Mean')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Negative Reviews\nBootstrap Distribution')
axes[1].legend()

# Difference distribution
axes[2].hist(diffs, bins=30, color='purple', alpha=0.7, edgecolor='black')
axes[2].axvline(np.mean(positive)-np.mean(negative),
                 color='purple', linestyle='-', linewidth=2, label='Observed diff')
axes[2].axvline(diff_ci[0], color='orange', linestyle='--', label='95% CI')
axes[2].axvline(diff_ci[1], color='orange', linestyle='--')
axes[2].axvline(0, color='gray', linestyle=':', alpha=0.5)
axes[2].set_xlabel('Bootstrap Difference')
axes[2].set_ylabel('Frequency')
axes[2].set_title('Difference (Positive - Negative)\nBootstrap Distribution')
axes[2].legend()

plt.tight_layout()
plt.savefig('figures/bootstrap_distributions.png', dpi=100)
plt.show()

# POST HOC STRAT PLOT

sus_neg_reviews = df[(df['sentiment'] == 'neg') & (df['happiness_score'] > bootstrap_positive_mean)]
sus_pos_reviews = df[(df['sentiment'] == 'pos') & (df['happiness_score'] < np.mean(neg_means))]

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot ALL reviews as light background (optional - for context)
ax.scatter(df.index, df['happiness_score'], 
           alpha=0.1, color='gray', s=5, label='All Reviews')

# Plot suspicious negative reviews
if len(sus_neg_reviews) > 0:
    ax.scatter(sus_neg_reviews.index, sus_neg_reviews['happiness_score'], 
               color='red', edgecolor='black', s=50, alpha=0.7,
               label=f'Suspicious Negative (n={len(sus_neg_reviews)})')

# Plot suspicious positive reviews
if len(sus_pos_reviews) > 0:
    ax.scatter(sus_pos_reviews.index, sus_pos_reviews['happiness_score'], 
               color='blue', edgecolor='black', s=50, alpha=0.7,
               label=f'Suspicious Positive (n={len(sus_pos_reviews)})')

# Add threshold lines
ax.axhline(y=bootstrap_positive_mean, color='green', linestyle='--', 
           linewidth=2, label=f'Positive Mean: {bootstrap_positive_mean:.2f}')
ax.axhline(y=np.mean(neg_means), color='orange', linestyle='--', 
           linewidth=2, label=f'Negative Mean: {np.mean(neg_means):.2f}')

# Labels and title
ax.set_xlabel('Review Index', fontsize=12)
ax.set_ylabel('Happiness Score', fontsize=12)
ax.set_title('Suspicious Reviews: Crossing Sentiment Boundaries', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/suspicious_reviews_scatter.png", dpi=100)
plt.show()