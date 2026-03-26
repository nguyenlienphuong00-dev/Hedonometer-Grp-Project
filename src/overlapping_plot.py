import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('data/processed/imdb_reviews_scored.csv')

# Separate by sentiment
positive = df[df['sentiment'] == 'pos']['happiness_score'].values
negative = df[df['sentiment'] == 'neg']['happiness_score'].values

# Parameters
n_bootstrap = 1000
sample_size = 1000

# Storage
pos_means = []
neg_means = []
diffs = []
sus_neg_counts = []
sus_pos_counts = []


for i in range(n_bootstrap):
    # Sample WITH replacement
    pos_sample = np.random.choice(positive, size=sample_size, replace=True)
    neg_sample = np.random.choice(negative, size=sample_size, replace=True)
    
    # Means for THIS iteration
    pos_mean = np.mean(pos_sample)
    neg_mean = np.mean(neg_sample)
    
    # Store means (SINGLE numbers)
    pos_means.append(pos_mean)
    neg_means.append(neg_mean)
    diffs.append(pos_mean - neg_mean)
    
    # Suspicious reviews
    sus_neg = neg_sample[neg_sample > pos_mean]
    sus_neg_counts.append(len(sus_neg))
    
    sus_pos = pos_sample[pos_sample < neg_mean]
    sus_pos_counts.append(len(sus_pos))
    

# Calculate confidence intervals
pos_mean_est = np.mean(pos_means)
pos_ci = np.percentile(pos_means, [2.5, 97.5])

neg_mean_est = np.mean(neg_means)
neg_ci = np.percentile(neg_means, [2.5, 97.5])

diff_est = np.mean(diffs)
diff_ci = np.percentile(diffs, [2.5, 97.5])

# Print results
print("\n" + "="*50)
print("BOOTSTRAP RESULTS")
print("="*50)
print(f"Positive mean: {pos_mean_est:.3f} (95% CI: [{pos_ci[0]:.3f}, {pos_ci[1]:.3f}])")
print(f"Negative mean: {neg_mean_est:.3f} (95% CI: [{neg_ci[0]:.3f}, {neg_ci[1]:.3f}])")
print(f"Difference: {diff_est:.3f} (95% CI: [{diff_ci[0]:.3f}, {diff_ci[1]:.3f}])")

# Suspicious reviews
avg_sus_neg = np.mean(sus_neg_counts)
neg_ci_sus = np.percentile(sus_neg_counts, [2.5, 97.5])
print(f"\nSuspicious negative reviews (above positive mean):")
print(f"  Average per sample: {avg_sus_neg:.1f}")
print(f"  Percentage: {avg_sus_neg/sample_size*100:.1f}%")
print(f"  95% CI: [{neg_ci_sus[0]:.0f}, {neg_ci_sus[1]:.0f}]")

avg_sus_pos = np.mean(sus_pos_counts)
pos_ci_sus = np.percentile(sus_pos_counts, [2.5, 97.5])
print(f"\nSuspicious positive reviews (below negative mean):")
print(f"  Average per sample: {avg_sus_pos:.1f}")
print(f"  Percentage: {avg_sus_pos/sample_size*100:.1f}%")
print(f"  95% CI: [{pos_ci_sus[0]:.0f}, {pos_ci_sus[1]:.0f}]")

# Simple overlapping histograms
fig, ax = plt.subplots(figsize=(10, 6))
pos_means_array = np.array(pos_means)
neg_means_array = np.array(neg_means)

# Plot histograms with transparency
ax.hist(pos_means_array, bins=30, color='green', alpha=0.6, edgecolor='black', 
        density=True, label=f'Positive Reviews (mean = {pos_mean_est:.3f})')
ax.hist(neg_means_array, bins=30, color='red', alpha=0.6, edgecolor='black', 
        density=True, label=f'Negative Reviews (mean = {neg_mean_est:.3f})')

# Add mean lines
ax.axvline(pos_mean_est, color='darkgreen', linewidth=2, linestyle='-', 
           label=f'Positive Mean: {pos_mean_est:.3f}')
ax.axvline(neg_mean_est, color='darkred', linewidth=2, linestyle='-', 
           label=f'Negative Mean: {neg_mean_est:.3f}')

# Add difference annotation
diff = pos_mean_est - neg_mean_est
ax.text(0.95, 0.95, f'Difference: {diff:.3f}', 
        transform=ax.transAxes, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Mean Happiness Score')
ax.set_ylabel('Density')
ax.set_title('Distribution of Mean Happiness Scores: Positive vs Negative Reviews')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/bootstrap_means_overlap_simple.png', dpi=100)
plt.show()