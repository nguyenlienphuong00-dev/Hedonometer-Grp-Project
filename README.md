Table of contents:
- Project backstory, Provenance and Data acquisition
- Research question
- Technical pipeline 
- Methodology: Tokenization and Filtering
- Sampling plan and Bootstrap results
- Limitations 
- AI disclosure

Project backstory, Provenance and Data acquisition

​​The Backstory: Lexicon Exploration (labMT 1.0) 
Our research started off with an in-depth exploration of the labMT 1.0 dataset, while doing this we treated the lexicon itself as our primary object of study. By reconstructing the biography of its 10,222 words, we were able to identify the tensions within crowd-sourced sentiment. To be more specific, we analyzed contested terms with high rater disagreement, some examples of this are fucking, whiskey, and capitalism, which revealed how emotional meaning is often split by cultural, political, or age-related perspectives.

Reference: Dodds, Peter Sheridan, Kameron Decker Harris, Isabel M. Kloumann, Catherine A. Bliss, and Christopher M. Danforth. “Temporal Patterns of Happiness and Information in a Global Social Network: Hedonometrics and Twitter.” PLoS ONE 6, no. 12 (December 7, 2011): e26752. https://doi.org/10.1371/journal.pone.0026752.

Understanding these internal disagreements was of great importance before transitioning to using the Hedonometer as a measurement instrument. With this foundational knowledge of the lexicon’s strengths and biases, we moved from the theory of the lexicon to its application in a large-scale dataset.

The Provenance: IMDb Large Movie Review Dataset

Within this project, the IMDb Movie Review Dataset was used. This dataset consists of 50,000 reviews in total. Regarding the provenance of this data, it was originally collected and curated by Maas et al. (2011) from the Stanford AI Lab. To establish clear sentiment labels, Maas et al. (2011) filtered the data based on the users’ original out of 10-star ratings. A review was labeled negative if it scored 4 or lower, and positive if it scored 7 or higher. There is no neutral review in the dataset. The data is split into 25,000 training reviews and 25,000 testing reviews. The split of “testing” and “training” category is created to train their custom Word Vector Model and Linear Support Vector Machine (SVM) (Maas et al, 2011). Because we use the dataset for data visualization and exploratory analysis, this split does not affect our research. 

Maas, Andrew. “Sentiment Analysis,” n.d. https://ai.stanford.edu/~amaas/data/sentiment/.

Application and Suitability By comparing the lexicon's average happiness scores against these ground-truth movie ratings, we aimed to identify where the tool succeeds as a so called remote sensor of sentiment and where linguistic complexity, such as sarcasm or descriptive prose, causes the bag-of-words approach to fail. The IMDb dataset is suitable for this research because it provides clear sentiment labels for each user’s review. These labels can be used as a benchmark to evaluate if the Hedonometer happiness scores can produce similar sentiment interpretations. As the Hedonometer calculates happiness based on isolated word scores, the complex language, such as sarcasm, in movie reviews helps to examine the accuracy of the Hedonometer. Then we can identify and analyze linguistic patterns that appear in reviews where the word average happiness and the sentiment label do not match.
Data acquisition pipeline:
![pipeline 1](https://github.com/user-attachments/assets/cbf1aa2d-6a3c-48dd-8ae2-d60d2caf4851)




Research Question: How well do Hedonometer happiness scores align with IMDb sentiment labels, and what linguistic patterns characterize reviews where the two measures disagree?

Technical pipeline:
Data provenance:
![pipeline 2](https://github.com/user-attachments/assets/f3ebe937-4d97-46bd-9aa5-02b25dfeb46f)


Measurement:
![pipeline 3](https://github.com/user-attachments/assets/0caa6f31-1ddc-4378-acd6-e406245a8ea9)



Tokenization and Word Processing

To prepare the IMDb reviews for analysis, we first tokenized the text into individual words. Each review was converted to lowercase so that words like “Good” and “good” are treated the same. We then used a regular expression to extract only alphabetical words, removing punctuation and other symbols.



For example, the sentence:
- "This movie was amazing!"
becomes:
- ["this", "movie", "was", "amazing"]
This step is important because it standardizes the text and allows us to match words consistently with the sentiment lexicon.
![pipeline 5](https://github.com/user-attachments/assets/7ed1d8df-4494-4595-89fd-453f74ce8f3c)



Filtering and Cleaning Words

When we initially analyzed word frequencies, the most common words were not very meaningful (e.g., “this,” “one,” “”). These are common function words that appear frequently in language but do not carry sentiment.

To address this, we applied several filtering steps:
Removed standard stopwords such as “the,” “and,” and “have”
Removed additional high-frequency but uninformative words like “one,” “very,” and “people”
Excluded domain-specific words such as “movie” and “film,” which are common in reviews but do not reflect sentiment

<img width="1000" height="800" alt="suspicious_positive_words" src="https://github.com/user-attachments/assets/ecdfb773-e3af-446c-a0d2-379d2b88e340" />
<img width="1000" height="800" alt="suspicious_negative_words" src="https://github.com/user-attachments/assets/22a91438-e01e-4752-b6c9-d2c430fc04ef" />

Focusing on Emotional Words
To make the analysis more meaningful, we focused only on words with strong emotional content. Using the labMT scores, we kept words with happiness values ≤ 4 (negative) or ≥ 6 (positive), and excluded neutral words.
This helped remove generic or neutral terms and highlight words that actually express sentiment.

<img width="1000" height="800" alt="suspicious_positive_words_clean" src="https://github.com/user-attachments/assets/6d8e31bc-84f6-4e6c-aace-7418247213ad" />
<img width="1000" height="800" alt="suspicious_negative_words_clean" src="https://github.com/user-attachments/assets/9d1aad75-4b46-4900-9f94-64d0e5fb5c3a" />


Word Frequency Analysis
After cleaning the data, we computed the most frequent emotional words in the dataset. The final visualization shows words such as “good,” “bad,” “great,” and “love,” which better reflect how users express positive and negative opinions in reviews.
This approach provides a clearer view of the emotional language used in IMDb reviews and aligns with the goal of analyzing sentiment using the hedonometer.



Sampling Plan and Results
The dataset contains equal amounts of training, testing, positive, and negative reviews. The train/test category is present for model training, which is why we decided to not work with this category and view the dataset purely from sentiment and happiness score aspects. Sampling was done in these parts of the repository:

<img width="1186" height="429" alt="Screenshot 2026-03-26 at 23 47 59" src="https://github.com/user-attachments/assets/54fdd04e-4b1f-476c-9a99-99d4009ab02e" />


For our research, we want to make inferences on a population, which we defined as the IMDb dataset. We did not choose all reviews on the internet as our population, because our dataset does not include ‘neutrally sentiment’ reviews and our research question draws on reviews in the IMDb dataset, which were by humans chosen to be sentimentally strong.
<img width="1004" height="384" alt="Screenshot 2026-03-26 at 23 48 08" src="https://github.com/user-attachments/assets/d51b91d3-f801-43e4-9140-8ab603073a82" />


Via this pathway, we want to show our approach. To calculate the mean score of positive and negative reviews by using bootstrap, we resampled sample size of n=1000 one thousand times with replacement. Within the bootstrap we also investigated whether "rule-breaking" reviews exist - negative reviews with happiness scores above the positive mean, and positive reviews with happiness scores below the negative mean. 

<img width="1500" height="500" alt="bootstrap_means_histograms" src="https://github.com/user-attachments/assets/9ff016c6-06c1-4aa0-ac3b-3c1ce4101ef4" />
	Mean happiness scores of negative/positive reviews and the difference

We can be 95% confident that positive reviews score on average 6.116 [6.095, 6.136]while negative 5.750 [[5.728, 5.772]. For clarity purposes, the main results are visualized in a table:
<img width="1014" height="217" alt="Screenshot 2026-03-26 at 23 48 18" src="https://github.com/user-attachments/assets/7741753e-9628-435f-9941-2bb5a799de1a" />



The estimated difference-mean 0.367 indicates there is a difference of happiness between positive and negative reviews. However, the difference is not big, considering the scale range of the Hedonometer being 8 - this means the estimate has a significance of 4.59% within the scale range. 
The standard deviations of mean positive and negative score and difference moves around 0.01. This means our estimates do not have big variability and are stable.
SUSPICIOUS REVIEWS
Regarding rule-breaking reviews, our plots showcase an estimate mean of 132.6 suspicious negative and 136.9 suspicious negative reviews. The suspicious reviews are thus consistently present.

<img width="1200" height="500" alt="suspicious_counts_histograms" src="https://github.com/user-attachments/assets/72b25074-821d-4084-b968-cfa24d0decd1" />



Originally, we planned on combining the positive and negative mean distribution in hopes of seeing an overlap to indicate presence of suspicious reviews. However, this expectation was a miscalculation on our part and the result turned out to be different because the mean distribution, as said in its name, is a calculation of averages and not of individual reviews themselves. 

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/45c69308-51e4-4bae-8a7a-0ad8bd069b40" />


In spite of the miscalculation, we can observe in the combined mean distribution a clear and significant divergence between two sentiment categories with zero overlap, including the clear distinction of the confidence intervals. This demonstrates that positive reviews score higher on the Hedonometer than negative reviews. As a result, the sentiment labels match with the average happiness score. It can be seen that the Hedonometer is a powerful tool for measuring massive datasets.

<img width="1200" height="800" alt="image" src="https://github.com/user-attachments/assets/cb986b16-784b-475e-b135-f46b5ad9d80a" />


However, when we run a close-up sample of 1,000 reviews, a different pattern emerges. It can be seen that positive and negative reviews heavily overlap. Significantly, there are some negative reviews that score higher than the positive reviews and vice versa. The Hedonometer scores do not align with their sentiment labels, resulting in heavy overlap between average happiness score and sentiment labels.

WORDCLOUD
To take a closer look at the content of both types of suspicious reviews, we created a word cloud from 1,000 randomly sampled reviews that scored either above the mean of negative reviews (if positive) or below the mean of positive reviews (if negative).
Comparisons of suspicious positive & negative reviews: (replace this one with old one in the github)
Comparing the two word clouds shows a clear difference in how mismatches happen. Suspicious positive reviews mostly use neutral and descriptive words and do not include many strongly positive terms. In contrast, suspicious negative reviews often mix negative and positive language, where some praise appears together with criticism. This means that mismatches occur in different ways for the two groups. For positive reviews, mismatches happen in different ways for the two groups. For positive reviews, mismatches are mainly caused by weak or driven by weak or limited positive language. For negative reviews, they are caused by the use of mixed or partly positive expressions. Overall, this comparison shows that the hedonometer reacts strongly to clearly positive or negative words, but it does not capture more subtle meanings that depend on context or sentence structure.
<img width="1200" height="600" alt="suspicious_positive_wordcloud" src="https://github.com/user-attachments/assets/5d755193-15c5-408c-aa08-4c811b71ed45" />
<img width="1200" height="600" alt="suspicious_negative_wordcloud" src="https://github.com/user-attachments/assets/d65b865a-3815-4f3f-a4c4-4e731967a45e" />


Limitations
The method relies on a predefined lexicon (labMT), which means that any words not included in the dataset are ignored. This can lead to a loss of meaning, especially when important descriptive words are missing from the lexicon.
The analysis treats text as a collection of individual words (a “bag-of-words” approach), meaning that context is not considered. As a result, phrases like “not good” may be incorrectly interpreted as positive because the word “good” is included without accounting for negation.
The filtering process, while necessary, may remove some relevant words. For example, excluding common or domain-specific words like “movie” and “film” improves clarity, but also removes part of the natural structure of reviews.
Although focusing on emotionally strong words improves interpretability, it simplifies the data by removing neutral language. This means the analysis captures general sentiment trends rather than the full nuance of how people express opinions.

AI-use disclosure:
AI Disclosure and Statement of Use
We disclose the use of Large Language Models (LLMs), specifically Gemini Pro (Google), DeepSeek, and ChatGPT (OpenAI), as supporting tools used throughout making this project. We used different AI-models for the following reasons:
Logic and Debugging, DeepSeek a ChatGPT: We utilized DeepSeek and ChatGPT to assist in writing Python scripts for data cleaning and to optimize the looping logic for the 1,000x bootstrap resampling. These tools helped troubleshoot syntax errors and ensure computational efficiency.
Structural Organization and Communication, Gemini Pro: Gemini Pro was used to help brainstorm the Backstory narrative in order to make the project coherent and to organize our README into a professional, scannable format.
Data Interpretation and Synthesis: While AI suggested ways to visualize our results (explaining the difference between frequency and density), all final interpretations, the identification of contested words, and the analysis of the 13.5% sentiment overlap are the original intellectual work of the student team.
Content Refining: AI acted as a peer editor to ensure grammatical correctness and clarity in our written documentation.

Roles

Mila: readme
Ran: tokenization, analyzing suspicious reviews, interpreting limitations
Grace: Word Cloud
Quynh: Dataset clarification, interpretation of random sample and bootstrapping distribution histogram.
Petra: Sampling and Inference plots







The Data Provenance Pipeline
Use this in the Data Acquisition section to show how you handled the 50,000 reviews 

The Measurement Pipeline
Use this in the Hedonometer Measurement Method section to show how you turned text into happiness scores.
The Inference & Visualization Pipeline
Use this in the Sampling Plan and Results section to show how you got your final statistics and the boxplot.




https://docs.google.com/document/d/1FrWt4zHO6LolhVFs1XpoWNObe1gRzSD37RYbAfmTcR8/edit?tab=t.0


