# Hedonometer-Grp-Project
1.1 Loading the file
We used df_read.csv to read the txt. file into a pandas dataframe.In order to convert all columns into numeric types, we used na_values and listed "--" to be perceived as Not a Number (NaN). In the end we converted te txt. file into a csv with df.to_csv. (Due to a mistaken manipulation of folders in the local, the cleaned csv. dataset was uploaded via the GitHub interface)
   
The dataset contains 8 columns and 10222 rows excluding the header. Each of last four columns (twitter_rank, google_rank, nyt_rank_lyrics) have 5222 values missing: Dodds et al. clarify that they only ranked the top 5000 frequent words.

1.1 Data dictionary:
- word: what word is being rated/inspected (string)
- happiness_rank: ranking from indicating most happiness to least (integer)
- happiness_average: the average score of how close to 'happiness' the word is, made by AMT (float)
- happienss_standard_deviation: how much disagreement there is to this crowd-sourced ranking from the rest of the crowd (float)
- twitter_rank: frequency ranking (float)
- google_rank: frequency ranking (float)
- nyt_rank: frequency ranking (float)
- lyrics: frequency ranking (float)


1.2 Sanity checks
Regarding data quality, there are no duplicates and the word format (spacing, lowercase) stays consistent. Word selection seems to encompass wide spectrum of meanings - every day objects, terminology, verbs, adjectives, material and abstract etc. Although, there are no duplicates, half of the top 10 happiness-indicating words stem from the core 'laugh': verb - base, continous, past forms - and the noun. One could view this as a downgrade to the data quality, however, as deviations of the same core hold differing scores, one can argue they might hold some relevance to their perception
.
Most of the top ten 'happiness' words are unarguably ones we would expect. Interestingly, laughter tops the word happiness itself, perhaps because of it being an act embodying the feeling, affording us to give it a material reality. 
The least happiness containing words are connotated with death, which has its own happiness score. Interestingly, suicide ranks higher in negativity than other forms/directions of killing. Personally, I also understand that rape is ranked to be more negative than acts of killing due to its gruesome nature.