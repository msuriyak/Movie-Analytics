import urllib
from urllib import request as rs
from bs4 import BeautifulSoup as bs
import re
import json
import sys
import socket

class RTScrape(object):
    # title of the movie
    title = None
    year= None
    # RT URL of the movie
    url = None
    # RT tomatometer rating of the movie
    tomatometer_all_critics_rating = None
    tomatometer_all_average_rating = None
    tomatometer_all_reviews_counted = None
    tomatometer_all_fresh = None
    tomatometer_all_rotten = None

    tomatometer_top_critics_rating = None
    tomatometer_top_average_rating = None
    tomatometer_top_reviews_counted = None
    tomatometer_top_fresh = None
    tomatometer_top_rotten = None
    # RT audience rating of the movie
    audience = None
    audience_average_rating = None
    audience_user_ratings= None
    # Did we find a result?
    found = False

    # for fetching webpages
    # constant
    BASE_URL = 'http://www.rottentomatoes.com'
    SEARCH_URL = '%s/search/?search=' % BASE_URL

    def __init__(self, title, year):
        self.query_title = title
        self.query_year = year
        self._process()

    def _search_movie(self, timeout=10):
        print('Searching !!')
        utitle = urllib.parse.quote(self.query_title)
        url = self.SEARCH_URL + utitle

        try :
            page = rs.urlopen(url, timeout=timeout)
        except socket.timeout:
            self.timeout = 1
            raise RuntimeError('Timeout')
        soup = bs(page, 'html.parser')
        
        int_res = soup.findAll('script')

        for item in int_res:
            if len(item.contents) > 0:
                if "search-results-root" in item.contents[0]:
                    search_results = item.contents[0]

        Movie_info = re.search('([^{]*)"year":(%s),"url":"(/m[^,]+)"' % self.query_year, search_results)
        if Movie_info == None:
            print('No matches found !!')
            return None
        else :
            print('Matches found !!')

        movie_url = self.BASE_URL + Movie_info.group(3)

        return movie_url

    def _process(self, timeout=10):
        url = self._search_movie()
        if url == None :
            msg = 'No matching results !! Exiting with all values set to None'
            return
        self.url = url
        try :
            page = rs.urlopen(url, timeout=timeout)
        except socket.timeout:
            self.timeout = 1
            raise RuntimeError('Timeout')
        soup = bs(page, 'html.parser')

        self.title = soup.find('h1', {'data-type' : 'title'}).text.strip() 
        
        self.year = int(self.title.split(' ')[-1][1:-1])
        self.title = ' '.join(self.title.split(' ')[:-1])

        # Tomatometer Ratings
        try :
            self.tomatometer_all_critics_rating = soup.find('div', {'class' : 'tab-pane active', 'id' : 'all-critics-numbers'}).find('span',{'class':'meter-value superPageFontColor'}).find('span').contents[0]
        except AttributeError:
            self.tomatometer_all_critics_rating = None
        int_res = soup.find('div', {'class' : 'tab-pane active', 'id' : 'all-critics-numbers'}).findAll('div',{'class':'superPageFontColor'})
        ctr = 1
        for item in int_res:
            if ctr == 1:
                self.tomatometer_all_average_rating = float(item.contents[-1].strip().split('/')[0])
                ctr += 1
            elif ctr == 2:
                self.tomatometer_all_reviews_counted = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr += 1;
            elif ctr == 3:
                self.tomatometer_all_fresh = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr += 1;
            elif ctr == 4:
                self.tomatometer_all_rotten = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr = 1;
        try :
            self.tomatometer_top_critics_rating = soup.find('div', {'class' : 'tab-pane', 'id' : 'top-critics-numbers'}).find('span',{'class':'meter-value superPageFontColor'}).find('span').contents[0]
        except AttributeError:
            self.tomatometer_top_critics_rating = None
        int_res = soup.find('div', {'class' : 'tab-pane', 'id' : 'top-critics-numbers'}).findAll('div',{'class':'superPageFontColor'})
        for item in int_res:
            if ctr == 1:
                self.tomatometer_top_average_rating = float(item.contents[-1].strip().split('/')[0])
                ctr += 1
            elif ctr == 2:
                self.tomatometer_top_reviews_counted = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr += 1;
            elif ctr == 3:
                self.tomatometer_top_fresh = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr += 1;
            elif ctr == 4:
                self.tomatometer_top_rotten = int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                ctr = 1;

        self.audience = soup.find('div', {'class' : 'audience-score meter'}).find('span', {'class':'superPageFontColor', 'style':'vertical-align:top'}).contents[0][:-1]
        int_res = soup.find('div', {'class' : 'audience-info hidden-xs superPageFontColor'}).findAll('div')
        for item in int_res:
            if ctr == 1:
                self.audience_average_rating = float(item.contents[-1].strip().split('/')[0])
                ctr += 1
            elif ctr == 2:
                self.audience_user_ratings = int("".join(item.contents[-1].strip().split(',')))
                ctr = 1;

    def make_json(self):

        result = {"Ratings (all)"             : self.tomatometer_all_critics_rating,
                  "Average Rating (all)"      : self.tomatometer_all_average_rating,
                  "Reviews Counted (all)"     : self.tomatometer_all_reviews_counted,
                  "Fresh (all)"               : self.tomatometer_all_fresh,
                  "Rotten (all)"              : self.tomatometer_all_rotten,
                  "Ratings (top)"             : self.tomatometer_top_critics_rating,
                  "Average Rating (top)"      : self.tomatometer_top_average_rating,
                  "Reviews Counted (top)"     : self.tomatometer_top_reviews_counted,
                  "Fresh (top)"               : self.tomatometer_top_fresh,
                  "Rotten (top)"              : self.tomatometer_top_rotten,
                  "Score (audience)"          : self.audience,
                  "Average Rating (audience)" : self.audience_average_rating,
                  "User Ratings (audience)"   : self.audience_user_ratings,
                  "Movie"                     : self.title,
                  "Year"                      : self.year
                  }

        return json.dumps(result)

if __name__ == "__main__":
    print('Running main!!!')
    #print(RTScrape('logan', 2017).make_json())
    print(RTScrape('The Thief', 1952).make_json())