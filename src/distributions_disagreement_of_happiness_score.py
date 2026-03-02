import pandas as pd
import matplotlib.pyplot as plt # Importing the matplotlib library for plotting and setting the nickname to save typing.

df = pd.read_csv(r'C:\Users\ASUS ZenBook\Desktop\coding-humanities\hedonometer_project\Hedonometer-Grp-Project\data\dataset.txt', sep = '\t', skiprows = 2, na_values = '--')
print("Dataset loaded successfully!")
print(df.head())
# Check if dataset is loaded correctly.

#2.1

# Do the math (summary statistics).
mean_val = df['happiness_average'].mean() #calcukating the mean of the happiness scores.
median_val = df['happiness_average'].median() #calculating the median of the happiness scores.
std_val = df['happiness_average'].std() #calculating the standard deviation of the happiness scores.
perc_5th = df['happiness_average'].quantile(0.05) #calculating the 5th percentile of the happiness scores.
perc_95th = df['happiness_average'].quantile(0.95) #calculating the 95th percentile of the happiness scores.
print(f"Mean happiness score: {mean_val:.2f}")
print(f"Median happiness score: {median_val:.2f}")
print(f"Standard deviation of happiness score: {std_val:.2f}")
print(f"5th percentile of happiness score: {perc_5th:.2f}")
print(f"95th percentile of happiness score: {perc_95th:.2f}")

# Histogram of happiness scores.
plt.figure(figsize=(10, 6)) #create a blank canvas that is 10 inches wide and 6 inches tall for better visualization.
plt.hist(df['happiness_average'], bins = 50, color='skyblue', edgecolor='black') #bins=50,Python divide the range of happiness scores into 50 equal intervals, color makes the bars blue, and edgecolor puts a black outline around them so they are easy to see.

plt.title('Distribution of Happiness Scores') #title of the historgram.
plt.xlabel('Happiness Score (1 to 9)') #label for x-axis.
plt.ylabel('Frequency (Number of words)') #label for y-axis.
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f"mean: {mean_val:.2f}") #add a vertical dashed red line at the mean value of happiness scores, with a label showing the mean value.
plt.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label=f"median: {median_val:.2f}") #add a vertical dashed green line at the median value of happiness scores, with a label showing the median value.
plt.legend() #creates a little key in the corner so people know what the red and green lines mean.

plt.savefig(r'C:\Users\ASUS ZenBook\Desktop\coding-humanities\hedonometer_project\Hedonometer-Grp-Project\figures\happiness_histogram.png') #save the histogram as a PNG file in the specified location.
plt.show() #display the histogram.

#2.2
# Disagreement and Scatterplot.
top_contested = df.sort_values(by='happiness_standard_deviation', ascending=False).head(15) #sort the dataset by the standard deviation of happiness scores in descending order and select the top 15 words with the highest disagreement.
print(top_contested[['word', 'happiness_average', 'happiness_standard_deviation']])

plt.figure(figsize =(10,6)) #create a blank canvas that is 6 inches wide and 10 inches tall for better visualization.
plt.scatter(df['happiness_average'],df['happiness_standard_deviation'], color='green', alpha=0.4, s=15) #create a scatter plot with happiness average on the x-axis and standard deviation on the y-axis, using purple dots that are slightly transparent (alpha=0.4) and small in size (s=15).
plt.title('Words Happiness vs Disagreement') #title of the scatter plot.
plt.xlabel('Average Happiness Score (1 to 9)') #label for x-axis.
plt.ylabel('Standard Deviation of Happiness Score (Disagreement)') #label for y-axis.
plt.grid(True, linestyle= '--', alpha=0.5) #add a grid to the scatter plot with dashed lines and light transparency for better readability.
plt.savefig(r'C:\Users\ASUS ZenBook\Desktop\coding-humanities\hedonometer_project\Hedonometer-Grp-Project\figures\happiness_scatter.png') #save the scatter plot as a PNG file in the specified location.
plt.show() #display the scatter plot.
