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


# ============================================
# HISTOGRAM 1: Mean Estimates with Confidence Intervals
# ============================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Positive means
pos_means_array = np.array(pos_means)
n, bins, patches = axes[0].hist(pos_means_array, bins=30, align = 'mid', color='green', alpha=0.7, edgecolor='black')

# Add vertical lines
axes[0].axvline(pos_mean_est, color='darkgreen', linewidth=2, linestyle='-', 
                label=f'Mean: {pos_mean_est:.3f}')
axes[0].axvline(pos_ci[0], color='red', linestyle='--', linewidth=1.5, 
                label='95% CI')
axes[0].axvline(pos_ci[1], color='red', linestyle='--', linewidth=1.5)

# Get y-axis limits after histogram
ylim = axes[0].get_ylim()

# Fill confidence interval region
axes[0].fill_betweenx([0, ylim[1]], pos_ci[0], pos_ci[1], 
                       alpha=0.2, color='gray', label='CI Region')

# Set labels and title
axes[0].set_xlabel('Mean Happiness Score')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Positive Reviews')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Negative means
axes[1].hist(neg_means, bins=30, color='red', alpha=0.7, edgecolor='black')
axes[1].axvline(neg_mean_est, color='darkred', linewidth=2, linestyle='-', 
                label=f'Mean: {neg_mean_est:.3f}')
axes[1].axvline(neg_ci[0], color='blue', linestyle='--', linewidth=1.5, 
                label=f'95% CI')
axes[1].axvline(neg_ci[1], color='blue', linestyle='--', linewidth=1.5)
ylim = axes[1].get_ylim()
axes[1].fill_betweenx([0, ylim[1]], neg_ci[0], neg_ci[1], 
                       alpha=0.2, color='gray', label='CI Region')
axes[1].set_xlabel('Mean Happiness Score')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Negative Reviews')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Plot 3: Differences
axes[2].hist(diffs, bins=30, color='purple', alpha=0.7, edgecolor='black')
axes[2].axvline(diff_est, color='darkviolet', linewidth=2, linestyle='-', 
                label=f'Diff: {diff_est:.3f}')
axes[2].axvline(diff_ci[0], color='orange', linestyle='--', linewidth=1.5, 
                label=f'95% CI')
axes[2].axvline(diff_ci[1], color='orange', linestyle='--', linewidth=1.5)
axes[2].axvline(0, color='gray', linestyle=':', linewidth=1.5, alpha=0.5)
ylim = axes[2].get_ylim()
axes[2].fill_betweenx([0, ylim[1]], diff_ci[0], diff_ci[1], 
                       alpha=0.2, color='gray', label='CI Region')
axes[2].set_xlabel('Difference (Positive - Negative)')
axes[2].set_ylabel('Frequency')
axes[2].set_title('Difference in Means')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/bootstrap_means_histograms.png', dpi=100)
plt.show()

# ============================================
# HISTOGRAM 2: Suspicious Reviews Counts
# ============================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Suspicious negative counts
axes[0].hist(sus_neg_counts, bins=30, color='orange', alpha=0.7, edgecolor='black')
axes[0].axvline(avg_sus_neg, color='red', linewidth=2, linestyle='-', 
                label=f'Average: {avg_sus_neg:.1f}')
axes[0].axvline(neg_ci_sus[0], color='blue', linestyle='--', linewidth=1.5, 
                label=f'95% CI')
axes[0].axvline(neg_ci_sus[1], color='blue', linestyle='--', linewidth=1.5)
ylim = axes[0].get_ylim()
axes[0].fill_betweenx([0, ylim[1]], neg_ci_sus[0], neg_ci_sus[1], 
                       alpha=0.2, color='gray', label='CI Region')
axes[0].set_xlabel('Number of Suspicious Reviews')
axes[0].set_ylabel('Frequency')
axes[0].set_title(f'Suspicious Negative Reviews\n(Negative > Positive Mean)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Suspicious positive counts
axes[1].hist(sus_pos_counts, bins=30, color='purple', alpha=0.7, edgecolor='black')
axes[1].axvline(avg_sus_pos, color='red', linewidth=2, linestyle='-', 
                label=f'Average: {avg_sus_pos:.1f}')
axes[1].axvline(pos_ci_sus[0], color='blue', linestyle='--', linewidth=1.5, 
                label=f'95% CI')
axes[1].axvline(pos_ci_sus[1], color='blue', linestyle='--', linewidth=1.5)
ylim = axes[1].get_ylim()
axes[1].fill_betweenx([0, ylim[1]], pos_ci_sus[0], pos_ci_sus[1], 
                       alpha=0.2, color='gray', label='CI Region')
axes[1].set_xlabel('Number of Suspicious Reviews')
axes[1].set_ylabel('Frequency')
axes[1].set_title(f'Suspicious Positive Reviews\n(Positive < Negative Mean)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/suspicious_counts_histograms.png', dpi=100)
plt.show()

#### example neg scores of one n=1000 sample
np.random.seed(42)
random_sample = df.sample(n=1000, replace=False, random_state=42)

# Separate positive and negative reviews
pos_sample2 = random_sample[random_sample['sentiment'] == 'pos']['happiness_score']
neg_sample2 = random_sample[random_sample['sentiment'] == 'neg']['happiness_score']

# Calculate means
pos_mean2 = pos_sample2.mean()
neg_mean2 = neg_sample2.mean()

# Create figure with histogram and text summary
fig, ax = plt.subplots(figsize=(12, 8))

# Plot histograms
ax.hist(pos_sample2, bins=30, color='green', alpha=0.6, edgecolor='black', 
        label=f'Positive Reviews (n={len(pos_sample2)}, mean={pos_mean2:.3f})')
ax.hist(neg_sample2, bins=30, color='red', alpha=0.6, edgecolor='black', 
        label=f'Negative Reviews (n={len(neg_sample2)}, mean={neg_mean2:.3f})')

# Add vertical lines
ax.axvline(pos_mean2, color='darkgreen', linewidth=2, linestyle='-', 
           label=f'Positive Mean: {pos_mean2:.3f}')
ax.axvline(neg_mean2, color='darkred', linewidth=2, linestyle='-', 
           label=f'Negative Mean: {neg_mean2:.3f}')

# Highlight negative reviews above positive mean
#neg_above = neg_sample2[neg_sample2 > pos_mean2]
#if len(neg_above) > 0:
 #   ax.hist(neg_above, bins=30, color='orange', alpha=0.5, edgecolor='black',
  #          label=f'Negative > Positive Mean (n={len(neg_above)})')

ax.set_xlabel('Happiness Score')
ax.set_ylabel('Frequency')
ax.set_title(f'Random Sample of 1000 Reviews\nPositive Mean: {pos_mean2:.3f} | Negative Mean: {neg_mean2:.3f}')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
plt.savefig('figures/sample.png', dpi=100)