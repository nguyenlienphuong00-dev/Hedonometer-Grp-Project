# Hedonometer-Grp-Project
2.1. Distribution of Happiness Scores. 

Mean happiness score: 5.38
Median happiness score: 5.44
Standard deviation of happiness score: 1.08
5th percentile of happiness score: 3.18
95th percentile of happiness score: 7.08

Interpretation: 
Looking at the histogram, the happiness scores are slightly above neutral with the highest concentration of words between 5 and 6. The mean which is 5.38 and the median which is 5.44 are close. This shows a symmetric distribution. However, the mean is smaller than the median because it is pulled down by an amount of negative words on the left side of the chart. The left tail is longer than the right one, emphasizing the mild left-skewed distribution. Despite the majority of neutral and positive words, the negative words extend the lower end of the scale. Most of the tallest blue bars are centered between 4.5 and 6.5 scores. Many words in the middle of the bar chart are considered neutral by people. The surprising pattern is that no word gets an absolute score such as 1 or 9. It is interesting that out of numerous words, people were unable to agree on any words that are absolutely positive or negative. 

2.2 Top 5 contested words.
                word  happiness_average  happiness_standard_deviation
8425         fucking               4.64                        2.9260  
8019           pussy               4.80                        2.6650
3769         whiskey               5.72                        2.6422
6389      capitalism               5.16                        2.4524
8796       mortality               4.38                        2.5546

Interpretation: 
- 'Fucking' is considered highly negative and aggressive in its meaning. Some people use it to curse or swear at other people, so it gets a low score. However, in modern society, it is also used as a positive intensifier to express an individual's feelings such as "This is fucking amazing!". Therefore, young teenagers rate this word with high score, creating a massive contradiction in data.

- The reason for the disagreement over 'Pussy' is that it has various conflicting meanings. According to English dictionaries, it can be a harmless word for a cat. Otherwise, it can have vulgar slang meanings, such as a woman's genital or a weak and cowardly man. With each meaning that has different scores, this word becomes controversial.

- 'Whiskey' has many disagreements due to differences in culture. Many individuals consider whiskey a drink for entertainment, relaxation, and socialization, so they rate it with a positive score. While the others associate whiskey with alcoholism and destructive behaviors, giving it a low score. 

- The word 'Capitalism' is a political and economic term. It creates a controversial conversation because of the distinction in ideologies among individuals. Depending on the rater's politics, it can refer to wealth, freedom and innovation or greed, poverty and inequality.

- 'Mortality' is chosen to be in the top 5 of contested words in data. For some people, mortality can bring them many benefits such as long life, power and experience. They will give a high score to this word. However, the others link this word with loneliness, death and loss. They think when they become mortal, they have to watch their beloveds die. This leads to a low score. The opposite perspectives creates the contradictory data. 

Connecting qualitative interpretation to quantitative pattern:

In the scatterplot, a fascinating pattern emerges. The words with the highest standard deviation scores have average happiness scores centering in the middle of bar chart. The scatterplot shows that the highest dots are clustered in the center between 5 and 6. This creates a mathematical sense because these words are divided. They received many low scores from individuals who hate them and numerous high scores from people who have positive impressions of them. When we average those opposite data together, they cancel each other out, creating the final score that seems to be neutral.


![Corpus comparison](figures/corpus_counts.png)

Each corpus contributes 5000 words to the labMT dataset. However, overlap is incomplete: only 1,816 words appear in all four corpora. This demonstrates that “common language” depends on platform and genre.
