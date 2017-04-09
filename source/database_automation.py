import pandas as pd
import numpy as np
from IMDb_scraper import IMDb
from RTScraper import RTScrape
import os 
import sys
import json

def make_data(data, i):
    imdb = data['imdb']
    rt = data['rotten tomatoes']
    res = str(i) + ';'
    for value in list(imdb.values()) + list(rt.values()):     
        if type(value) == list:
            res += ' | '.join(value) + ';'
        else :
            res += str(value) + ';'
    res = res[:-1] + '\n'
    return res


movies = pd.read_csv('../data/Datasets/name_and_year.csv')

data = {}
f = open('results', 'w')
for i in range(1):
    name = movies.iloc[i]['Name']
    year = int(movies.iloc[i]['Year'])
    
    print(i, ' : ', name, '(', year,')')

    try :
        print('\nIMDb ...')
        temp = IMDb()
        temp.collect_data(name, year)
        imdb_data = json.loads(temp.make_json())

        print('\nRotten Tomatoes ...')
        rt_data = json.loads(RTScrape(name, year).make_json())
        data = {'imdb' : imdb_data, 'rotten tomatoes' : rt_data}
        print('\n')

        if i == 0:
            temp = ';' + 'imdb;'*len(imdb_data.keys()) + 'rotten tomatoes;'*len(rt_data.keys())
            temp = temp[:-1] + '\n'
            f.write(temp)

            temp = 'Serial No.;'
            for key in imdb_data.keys():
                temp += str(key) + ';'
            for key in rt_data.keys():
                temp += str(key) + ';'
            temp = temp[:-1] + '\n'
            f.write(temp)

        f.write(make_data(data, i))

    except Exception as e :
        temp = [str(i), name, str(year), str(e)]
        print('\t******* Failed !!! *******')
        print(';'.join(temp), file=sys.stderr)

'''
0   None    Montgomery Clift | Elizabeth Taylor | Shelley Winters | Anne Revere | Keefe Brasselle | Fred Clark | Raymond Burr | Herbert Heyes | Shepperd Strudwick | Frieda Inescort | Kathryn Givney | Walter Sande | Ted de Corsia | John Ridgely | Lois Chartrand    1951-08-14  A Place in the Sun  NA  7.8 tt0043924   None    $2,295,304  Drama | Romance English 122 min USA 1951    15816   None    Theodore Dreiser | Patrick Kearney  George Stevens  28  None    None    75  None    7.2 84  21  None    1951    7   None    3.9 A Place in the Sun  8458
'''