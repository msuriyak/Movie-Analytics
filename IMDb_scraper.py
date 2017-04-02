from __future__ import division
import urllib
from bs4 import BeautifulSoup as bs
import re
import json
from oscar_movies import *

class IMDb(object):
    def __init__(self, title='', year='', lang='en'):
        self.title_query = title
        self.year_query = year
        self.language_query = lang

    def search_title(self, title, year, lang='en', production_status='released', title_type='feature', max_attempts=3, timeout=1.5):
        link = 'http://www.imdb.com/search/title?'
        param = urllib.parse.urlencode({'title' : title, 
                                        'production_status' : production_status, 
                                        'release_date' : repr(year) + ',', 
                                        'languages' : lang, 
                                        'title_type' : title_type})
        link = link + param
        print('Searching ...')
        attempts = 0
        while attempts < max_attempts :
            attempts += 1
            try :
                html = urllib.request.urlopen(link, timeout=timeout)
                print('Matches found!!!')
                break
            except Exception as e :
                msg = ('Search attempt %d failed with ' %(attempts)) + str(e) + 'error'
                print(msg)
        
        if attempts == max_attempts :
            msg = 'Search failed after %d attempts' %(max_attempts)
            raise RuntimeError(msg)

        soup = bs(html, 'html.parser')
        if 'No results' in soup.find('div', {'class' : 'lister-item'}).text : 
            msg = 'No results found!!'
            raise RuntimeError(msg)
        movie_matches = soup.findAll('h3', { 'class' : 'lister-item-header' })  
        for movie in movie_matches :
            name = movie.find('a').text
            release_year = movie.find('span', {'class' : 'lister-item-year text-muted unbold'}).text
            if repr(year) in release_year :
                page_link = 'http://www.imdb.com' + movie.find('a').get('href')
        return page_link

    def collect_data(self, title='', year='', link='', max_attempts=2, timeout=3, timeout_search=3, max_attempts_search=2):
        if title == '' and year == '' and link == '' :
            msg = 'Year and title cannot be empty if URL is not provided'
            raise ValueError(msg)
        if link == '' :
                link = self.search_title(title, year, timeout=timeout_search, max_attempts=max_attempts_search)
        
        attempts = 0
        print('Retriving URL ...')
        while(attempts < max_attempts):
            attempts += 1
            try :
                html = urllib.request.urlopen(link, timeout=timeout)
                print('Successful connection')
                break
            except Exception as e:
                msg = ('Try %d, Exited with error ' %(attempts)) + str(e) 
                print(msg)
        
        if attempts == max_attempts :
            raise RuntimeError('Unable to collect data')

        soup = bs(html, 'html.parser')

        self.uid = soup.find('meta', {'property' : 'pageId'})['content']

        temp = soup.find('title')
        self.title = temp.text[:-14]
        self.year = temp.text[-12:-8]
        
        temp = soup.findAll('div', {'class' : 'credit_summary_item'})
        for item in temp:
            if 'Director' in item.find('h4', {'class' : 'inline'}).text:
                self.director = [person.find('span', {'class' : 'itemprop', 'itemprop' : 'name'}).text \
                                 for person in item.findAll('span', {'itemprop' : 'director'})]
            if 'Writer' in item.find('h4', {'class' : 'inline'}).text:
                self.writer   = [person.find('span', {'class' : 'itemprop', 'itemprop' : 'name'}).text \
                                 for person in item.findAll('span', {'itemprop' : 'creator'})]

        self.rating = float(soup.find('span', {'itemprop' : 'ratingValue'}).text)
        self.ratingCount = int(''.join(soup.find('span', {'class' : 'small', 'itemprop' : 'ratingCount'}).text.split(',')))
        try :
            self.metascore = int(soup.find('div', {'class' : 'metacriticScore score_favorable titleReviewBarSubItem'}).find('span').text)
        except Exception  as e:
            self.metascore = 'NA'

        table = soup.find('table', {'class' : 'cast_list'})
        self.cast = [actor.text for actor in table.findAll('span', {'class' : 'itemprop', 'itemprop' : 'name'})]
        
        temp = soup.findAll('div', {'class' : 'txt-block'}) 
        
        self.country = 'NA'  
        self.languages = 'NA'
        self.release_date = 'NA'
        self.budget = 'NA'
        self.opening_weekend = 'NA'
        self.gross = 'NA'
        self.runtime = 'NA'

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
        result = {'UID'             : self.uid,
                  'Title'           : self.title,
                  'Year'            : self.year, 
                  'Language'        : self.languages,
                  'Release Date'    : self.release_date,
                  'Director'        : self.director,   
                  'Writer'          : self.writer,
                  'Rating'          : self.rating,
                  'Rating Count'    : self.ratingCount,
                  'Metascore'       : self.metascore,
                  'Cast'            : self.cast,
                  'Country'         : self.country,
                  'Budget'          : self.budget,
                  'Opening weekend' : self.opening_weekend,
                  'Gross'           : self.gross,
                  'Runtime'         : self.runtime
                  }
        return json.dumps(result, indent=4, sort_keys=True)


if __name__ == '__main__' :    
    '''
    temp = IMDb()
    temp.collect_data('the rainmaker', 1997)

    print('\n')

    temp = IMDb()
    temp.collect_data('la la land', 2016)
    '''

    successful = []
    failed = []
    temp = IMDb()
    for item in get_all_oscar_movies():
        item = json.loads(item)
        if item['Winner'] == 1:
            try :
                temp.collect_data(item['Name'], item['Year'])
                successful.append(temp.make_json())
            except Exception as e :
                failed.append(item)
                print('\t\t\tFailed in %d' %(item['Year']))

    for item in failed:
        print(item['Year'])