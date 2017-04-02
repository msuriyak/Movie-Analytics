import urllib 
import re
import json
from bs4 import BeautifulSoup as bs

class movie():
    def __init__(self, title, year, winner, nominee):
        self.name = title
        self.year = year
        self.winner = winner
        self.nominee = nominee
    
    def make_csv(self):
        return "%s;%d;%d;%d" %(self.name, self.year, self.winner, self.nominee)

class critics_films():
    def __init__(self):
        self.scrape()
    
    
    def scrape(self):
        url='https://en.wikipedia.org/wiki/Independent_Spirit_Award_for_Best_Film'
        html = urllib.request.urlopen(url)
        soup = bs(html, 'html.parser')
        
        self.movie_list = []
        
        tables = soup.findAll('table', {'class' : 'wikitable'})
        for table in tables:
            rows = soup.findAll('tr')
            for row in rows:
                if row.find('td', {'rowspan' : '5'}) != None :
                    year = int(row.find('td', {'rowspan' : '5'}).find('a').contents[0])                
                title = row.find('i')
                if title != None :
                    title = title.find('a').contents[0]
                    if row.find('td', {'style' : 'background:#B0C4DE'}):
                        winner = 1
                        nominee = 1
                    else :
                        winner = 0
                        nominee = 1
                    self.movie_list.append(movie(title, year, winner, nominee).make_csv())
        
if __name__ == '__main__':
    print('Name;Year;Winner;Nominee')
    for film in critics_films().movie_list :
        print(film)