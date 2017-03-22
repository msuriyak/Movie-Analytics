from __future__ import division
import string
import numpy as np
import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs
import re
import json
import xml

class IMDb(object):
    def __init__(self, title='', year='', lang='en'):
        self.title_query = title
        self.year_query = year
        self.language_query = lang

    def search_title(self, title, year, lang='en', production_status='released', title_type='feature'):
        link = 'http://www.imdb.com/search/title?'
        param = urllib.parse.urlencode({'title' : title, 
        								'production_status' : production_status, 
        								'release_date' : repr(year) + ',', 
        								'languages' : lang, 
        								'title_type' : title_type})
        link = link + param
        print('Searching ...')
        html = urllib.request.urlopen(link)
        print('Matches found!!!')
        soup = bs(html, 'html.parser')
        movie_matches = soup.findAll('h3', { 'class' : 'lister-item-header' })  
        for movie in movie_matches :
            name = movie.find('a').text
            release_year = movie.find('span', {'class' : 'lister-item-year text-muted unbold'}).text
            if repr(year) in release_year :
                page_link = 'http://www.imdb.com' + movie.find('a').get('href')
        return page_link

    def collect_data(self, link='', title='', year=''):
    	if title == '' and year == '' and link == '' :
    		msg = 'Year and title cannot be empty if URL is not provided'
    		raise ValueError(msg)
    	if link == '' :
    		link = self.search_title(title, year)
    	

    	print('Retriving URL ...')
    	html = urllib.request.urlopen(link)
    	print('Successful connection')
    	soup = bs(html, 'html.parser')

    	self.uid = soup.find('meta', {'property' : 'pageId'})['content']

    	temp = soup.find('title')
    	self.title = temp.text[:-14]
    	self.year = temp.text[-12:-8]
    	
    	self.director = [person.find('span', {'class' : 'itemprop'}).text for person in soup.findAll('span', {'itemprop' : 'director'})]
    	self.writer   = [person.find('span', {'class' : 'itemprop'}).text for person in soup.findAll('span', {'itemprop' : 'creator'})]

    	self.rating = float(soup.find('span', {'itemprop' : 'ratingValue'}).text)
    	self.ratingCount = int(''.join(soup.find('span', {'class' : 'small', 'itemprop' : 'ratingCount'}).text.split(',')))
    	self.metascore = int(soup.find('div', {'class' : 'metacriticScore score_favorable titleReviewBarSubItem'}).find('span').text)

    	table = soup.find('table', {'class' : 'cast_list'})
    	self.cast = [actor.text for actor in table.findAll('span', {'class' : 'itemprop', 'itemprop' : 'name'})]
    	
    	temp = soup.findAll('div', {'class' : 'txt-block'}) 
    	#soup.findAll('h4', {'class' : 'inline'})
    	for item in temp :
    		term = item.find('h4', {'class' : 'inline'})
    		
    		if term == None :
    			continue
    		
    		term = term.text
    		if 'Country' in term :
    			self.country = [country.text for country in item.findAll('a')]
    		if 'Language'  in term :
    			self.languages = [lang.text for lang in item.findAll('a')]
    		if 'Release Date'  in term :
    			self.release_date = item.text[15:-22]
    		if 'Budget' in term:
    			self.budget = re.search('\$[0-9,]*', item.text).group()
    		if 'Opening Weekend' in term:
    			self.opening_weekend = re.search('\$[0-9,]*', item.text.strip()).group()
    		if 'Gross' in term:
    			self.gross = re.search('\$[0-9,]*', item.text.strip()).group()
    		if 'Runtime' in term:
    			self.runtime = item.find('time', {'itemprop' : 'duration'}).text

    def make_json(self):
    	result = {'UID' : self.uid,
    			  'Title' : self.title,
    			  'Year' : self.year, 
    			  'Language' : self.languages,
    			  'Release Date' : self.release_date,
    			  'Director' : self.director,	
    			  'Writer' : self.writer,
    			  'Rating' : self.rating,
    			  'Rating Count' : self.ratingCount,
    			  'Metascore' : self.metascore,
    			  'Cast' : self.cast,
    			  'Country' : self.country,
    			  'Budget' : self.budget,
    			  'Gross' : self.gross,
    			  'Runtime' : self.runtime
    			  }
    	return json.dumps(result, indent=4, sort_keys=True)


temp = IMDb()
link = temp.search_title('the rainmaker', 1997)
temp.collect_data(link)
print(temp.make_json())

print('\n')

temp = IMDb()
link = temp.search_title('la la land', 2016)
temp.collect_data(link)
print(temp.make_json())