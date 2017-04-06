import os
import pandas as pd
import numpy as np

######### Making necessary directories ######### 
if not os.path.exists('../Datasets'):
    os.makedirs('../Datasets')
    
# **************** Best Film ****************
gg = pd.read_csv('films_globe.csv', index_col=0)
res = []
for year in gg.index.unique():
    temp = gg.loc[year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
gg['Globe best film winner'] = res
gg['Globe best film nominee'] = 1
gg = gg.reset_index()[['Name', 'Year', 'Globe best film winner', 'Globe best film nominee']]

bf = pd.read_csv("films_bafta.csv", index_col=0)
res = []
for year in bf.index.unique():
    temp = bf.loc[year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
bf['BAFTA best film winner'] = res
bf['BAFTA best film nominee'] = 1
bf = bf.reset_index()
bf.columns = ['Year', 'Name'] + bf.columns[2:].tolist()

oscars = pd.read_csv('films_oscars.csv')

spirit = pd.read_csv('films_spirit.csv')

critic = pd.read_csv('films_critic.csv')
res = []
for year in critic['Year'].unique():
    temp = critic[critic['Year' ] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
critic['Critic best film winner'] = res
critic['Critic best film nominee'] = 1

df = [gg, bf, spirit, critic, oscars]
condition = ['Name', 'Year']
best_film = gg.merge(bf, how='outer', right_on=condition, left_on=condition)
for frame in df[2:]:
    best_film = best_film.merge(frame, how='outer', right_on=condition, left_on=condition)
best_film = best_film.fillna(0)
best_film.to_csv('../Datasets/best_film_consolidated.csv', index=False)

# **************** Best Actor ****************
gg = pd.read_csv('best_actor_globe.csv')
res = []
for year in gg['Year'].unique():
    temp = gg[gg['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
gg['Globe best actor winner'] = res
gg['Globe best actor nominee'] = 1
gg = gg[gg.columns[:2].tolist() + gg.columns[3:].tolist()]

bf = pd.read_csv('best_actor_bafta.csv')
res = []
for year in bf['Year'].unique():
    temp = bf[bf['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
bf['BAFTA best actor winner'] = res
bf['BAFTA best actor nominee'] = 1

spirit = pd.read_csv('best_actor_spirit.csv')
spirit = spirit[spirit.columns.tolist()[:-1]]
res = []
for year in spirit['Year'].unique():
    temp = spirit[spirit['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
spirit['Spirit best actor winner'] = res
spirit['Spirit best actor nominee'] = 1

guild = pd.read_csv('best_actor_guild.csv')
guild = guild[guild.columns.tolist()[:-1]]
res = []
for year in guild['Year'].unique():
    temp = guild[guild['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
guild['Guild best actor winner'] = res
guild['Guild best actor nominee'] = 1

oscars = pd.read_csv('oscar_actor.csv')
res = []
for year in oscars['Year'].unique():
    temp = oscars[oscars['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
oscars['Oscar best actor winner'] = res
oscars['Oscar best actor nominee'] = 1

df = [gg, bf, spirit, guild, oscars]
condition = ['Name', 'Year', 'Actor']
best_actor = gg.merge(bf, how='outer', right_on=condition, left_on=condition)
for frame in df[2:]:
    best_actor = best_actor.merge(frame, how='outer', right_on=condition, left_on=condition)
best_actor = best_actor.fillna(0)
best_actor.to_csv('../Datasets/best_actor_consolidated.csv', index=False)

# **************** Best Actress ****************
gg = pd.read_csv('best_actress_globe.csv')
res = []
for year in gg['Year'].unique():
    temp = gg[gg['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
gg['Globe best actress winner'] = res
gg['Globe best actress nominee'] = 1
gg = gg[gg.columns[:2].tolist() + gg.columns[3:].tolist()]

bf = pd.read_csv('best_actress_bafta.csv')
res = []
for year in bf['Year'].unique():
    temp = bf[bf['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
bf['BAFTA best actress winner'] = res
bf['BAFTA best actress nominee'] = 1

spirit = pd.read_csv('best_actress_spirit.csv')
spirit = spirit[spirit.columns.tolist()[:-1]]
res = []
for year in spirit['Year'].unique():
    temp = spirit[spirit['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
spirit['Spirit best actress winner'] = res
spirit['Spirit best actress nominee'] = 1

guild = pd.read_csv('best_actress_guild.csv')
guild = guild[guild.columns.tolist()[:-1]]
res = []
for year in guild['Year'].unique():
    temp = guild[guild['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
guild['Guild best actress winner'] = res
guild['Guild best actress nominee'] = 1

oscars = pd.read_csv('oscar_actress.csv')
res = []
for year in oscars['Year'].unique():
    temp = oscars[oscars['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
oscars['Oscar best actress winner'] = res
oscars['Oscar best actress nominee'] = 1

df = [gg, bf, spirit, guild, oscars]
condition = ['Name', 'Year', 'Actress']
best_actress = gg.merge(bf, how='outer', right_on=condition, left_on=condition)
for frame in df[2:]:
    best_actress = best_actress.merge(frame, how='outer', right_on=condition, left_on=condition)
best_actress = best_actress.fillna(0)
best_actress.to_csv('../Datasets/best_actress_consolidated.csv', index=False)

# **************** Best Director ****************
gg = pd.read_csv('direction_globe.csv')
res = []
for year in gg['Year'].unique():
    temp = gg[gg['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
gg['Globe best director winner'] = res
gg['Globe best director nominee'] = 1

bf = pd.read_csv('direction_bafta.csv')
res = []
for year in bf['Year'].unique():
    temp = bf[bf['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
bf['BAFTA best director winner'] = res
bf['BAFTA best director nominee'] = 1

spirit = pd.read_csv('direction_spirit.csv')
res = []
for year in spirit['Year'].unique():
    temp = spirit[spirit['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
spirit['Spirit best director winner'] = res
spirit['Spirit best director nominee'] = 1

oscars = pd.read_csv('oscar_director.csv')
res = []
for year in oscars['Year'].unique():
    temp = oscars[oscars['Year'] == year]
    if type(temp) == pd.core.series.Series:
        res += [1]
    else: 
        res += [1] + [0 for i in range(len(temp) -1 )]
res = np.array(res)
oscars['Oscar best director winner'] = res
oscars['Oscar best director nominee'] = 1

df = [gg, bf, spirit, oscars]
condition = ['Name', 'Year', 'Director']
best_director = gg.merge(bf, how='outer', right_on=condition, left_on=condition)
for frame in df[2:]:
    best_director = best_director.merge(frame, how='outer', right_on=condition, left_on=condition)
best_director = best_director.fillna(0)
best_director.to_csv('../Datasets/best_director_consolidated.csv', index=False)