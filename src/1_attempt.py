import pandas as pd

df = pd.read_csv("data/raw/Data_Set_S1.txt",
                 delimiter="\t",
                 skiprows=3,
                 na_values= ["--", ""])
df.to_csv("outputs/Data_Set_S1.csv", index=False) # index=False doesnt save row numbers as the first column - would move all columns to the right?

df = pd.read_csv("outputs/Data_Set_S1.csv")
print(df.dtypes)
print(df.info()) #or RangeIndex indicates rows, to confirm print(len(df)) is also possible
#print(df.describe())
print(df.isna().sum()) #gives what how many cells are empty

duplicates=df.duplicated(subset=["word"], keep=False) #looks at the word column, marking all duplicates as true
print(duplicates)
print(df[["word", "happiness_average"]].head(10))
#double brackets when selecting multiple columns, returning a dataframe
print(df[["word", "happiness_average"]].tail(10))


