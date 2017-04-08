import pandas as pd
import numpy as np

df1 = pd.read_csv('../../data/Datasets/best_film_consolidated.csv')
df2 = pd.read_csv('../../data/Datasets/best_director_consolidated.csv')
df3 = pd.read_csv('../../data/Datasets/best_actor_consolidated.csv')
df4 = pd.read_csv('../../data/Datasets/best_actress_consolidated.csv')

on = ['Name', 'Year']
df = df1.merge(df2, how='outer', left_on=on, right_on=on)
df = df.merge(df3, how='outer', left_on=on, right_on=on)
df = df.merge(df4, how='outer', left_on=on, right_on=on)

df.fillna(0)

df.drop_duplicates().to_csv('../../data/Datasets/consolidated.csv', index=False)

df[on].drop_duplicates().to_csv('../../data/Datasets/name_and_year.csv', index=False)