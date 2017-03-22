from __future__ import division
import numpy as np
import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs
import re
import json
import xml

class IMDb(object):
    def __init__(self, title='', year='', lang='English'):
        self.title_query = title
        self.year_query = year
        self.language_query = lang

    def search_title(self, title, year, lang='English'):
        link = 'http://www.imdb.com/find?'
        param = urllib.parse.urlencode({'q' : title, 'exact' : 'true', 's' : 'all'})
        link = link + param
        print('hey1')
        html = urllib.request.urlopen(link)
        print('hey2')
        soup = bs(html, 'html.parser')
        print('hey3')
        table = soup.find('table', { 'class' : 'findList' })  
        print('hey4')
        for row in table.findAll('tr') :
            name = row.find('td', {'class' : 'result_text' }).text
            if repr(year) in name :
                page_link = 'http://www.imdb.com' + row.find('a').get('href')
                print(page_link)
                

        

temp = IMDb()
temp.search_title('the rainmaker', 1997)

'''
from __future__ import division
import numpy as np
import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs
import re
import json
import xml

class IMDb(object):
    def __init__(self, title='', year='', lang='English'):
        self.title_query = title
        self.year_query = year
        self.language_query = lang

    def search_title(self, title, year, lang='en'):
        #link = 'http://www.imdb.com/find?'
        'http://www.imdb.com/search/title?&production_status=released&release_date=2017,&title=logan&title_type=feature'
        link = 'http://www.imdb.com/search/title?'
        param = urllib.parse.urlencode({'title' : title, 
                                        'release_date' : repr(year)+',', 
                                        'languages' : lang, 
                                        'title_type' : 'feature', 
                                        'production_status' : 'released'})
        link = link + param
        html = urllib.request.urlopen(link)
        soup = bs(html, 'html.parser')
        elements = soup.find_all('div', { 'class' : 'lister-list ' })  
        for item in soup.findAll('div', {'class' : 'lister-list'}) :
            #name = row.find('div', {'class' : 'lister-item mode-advanced' })\
            #          .find('div', {'class' : 'lister-item-content'})\
            #          .find('h3',  {'class' : 'lister-item-header'})
            #          .find('span', {'class' : 'lister-item-index unbold text-primary'})
            name = item.find
            if repr(year) in name :
                page_link = 'http://www.imdb.com' + row.find('a').get('href')
                print(page_link)
'''