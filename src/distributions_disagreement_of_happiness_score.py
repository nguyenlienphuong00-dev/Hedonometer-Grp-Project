import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv("data/raw/Data_Set_S1.txt", sep = '\t', skiprows = 2, na_values = '--')



#2.1

# Do the math (summary statistics).
mean_val = df['happiness_average'].mean() 
median_val = df['happiness_average'].median() 
std_val = df['happiness_average'].std() 
perc_5th = df['happiness_average'].quantile(0.05) 
perc_95th = df['happiness_average'].quantile(0.95) 
print(f"Mean happiness score: {mean_val:.2f}")
print(f"Median happiness score: {median_val:.2f}")
print(f"Standard deviation of happiness score: {std_val:.2f}")
print(f"5th percentile of happiness score: {perc_5th:.2f}")
print(f"95th percentile of happiness score: {perc_95th:.2f}")

# Histogram of happiness scores.
plt.figure(figsize=(10, 6)) 
plt.hist(df['happiness_average'], bins = 50, color='skyblue', edgecolor='black') 

plt.title('Distribution of Happiness Scores') 
plt.xlabel('Happiness Score (1 to 9)') 
plt.ylabel('Frequency (Number of words)')
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f"mean: {mean_val:.2f}") 
plt.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label=f"median: {median_val:.2f}") 
plt.legend() 
plt.savefig("figures/happiness_histogram.png")
plt.show() 

#2.2
# Disagreement and Scatterplot.
top_contested = df.sort_values(by='happiness_standard_deviation', ascending=False).head(15) 
print(top_contested[['word', 'happiness_average', 'happiness_standard_deviation']])

plt.figure(figsize =(10,6)) 
plt.scatter(df['happiness_average'],df['happiness_standard_deviation'], color='green', alpha=0.4, s=15) 
plt.title('Words Happiness vs Disagreement') 
plt.xlabel('Average Happiness Score (1 to 9)') 
plt.ylabel('Standard Deviation of Happiness Score (Disagreement)') 
plt.grid(True, linestyle= '--', alpha=0.5) 
plt.savefig("figures/happiness_scatter.png")
plt.show()

