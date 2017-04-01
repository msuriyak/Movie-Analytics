import urllib
from urllib import request as rs
from bs4 import BeautifulSoup as bs
import re
import json
import sys




class RTScrape():
    """Get the rating of a movie."""
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
    # Should we search and take the first hit?

    # constant
    BASE_URL = 'http://www.rottentomatoes.com'
    SEARCH_URL = '%s/search/?search=' % BASE_URL

    def __init__(self, title, year):
        self.title = title
        self.year = year
        self._process()

    def _search_movie(self):
        """Use RT's own search and return the first hit."""
        utitle=urllib.parse.quote(self.title)
        url = self.SEARCH_URL + utitle
        page = rs.urlopen(url)
        soup=bs(page, 'html.parser')
        int_res=soup.findAll('script')
        for item in int_res:
            if len(item.contents) > 0:
                if "search-results-root" in item.contents[0]:
                    search_results = item.contents[0]
        Movie_info=re.search('([^{]*)"year":(%s),"url":"(/m[^,]+)"' % self.year, search_results)
        movie_url=self.BASE_URL+Movie_info.group(3)


        return movie_url

    def _process(self):
        """Start the work."""

            # if search option is on => use RT's own search
        url = self._search_movie()

        try:
            self.url = url
            soup = bs( rs.urlopen(url), 'html.parser')
               ##Tomatometer Ratings


            self.tomatometer_all_critics_rating = soup.find('div', {'class' : 'tab-pane active', 'id' : 'all-critics-numbers'}).find('span',{'class':'meter-value superPageFontColor'}).find('span').contents[0]
            int_res=soup.find('div', {'class' : 'tab-pane active', 'id' : 'all-critics-numbers'}).findAll('div',{'class':'superPageFontColor'})
            ctr=1
            for item in int_res:
                if ctr==1:
                    self.tomatometer_all_average_rating=float(item.contents[-1].strip().split('/')[0])
                    ctr+=1
                elif ctr==2:
                    self.tomatometer_all_reviews_counted=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr+=1;
                elif ctr==3:
                    self.tomatometer_all_fresh=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr+=1;
                elif ctr==4:
                    self.tomatometer_all_rotten=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr=1;


            self.tomatometer_top_critics_rating = soup.find('div', {'class' : 'tab-pane', 'id' : 'top-critics-numbers'}).find('span',{'class':'meter-value superPageFontColor'}).find('span').contents[0]
            int_res=soup.find('div', {'class' : 'tab-pane', 'id' : 'top-critics-numbers'}).findAll('div',{'class':'superPageFontColor'})
            for item in int_res:
                if ctr==1:
                    self.tomatometer_top_average_rating=float(item.contents[-1].strip().split('/')[0])
                    ctr+=1
                elif ctr==2:
                    self.tomatometer_top_reviews_counted=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr+=1;
                elif ctr==3:
                    self.tomatometer_top_fresh=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr+=1;
                elif ctr==4:
                    self.tomatometer_top_rotten=int(re.search('>(.+)<',str(item.contents[-2])).group(1))
                    ctr=1;

            self.audience = soup.find('div', {'class' : 'audience-score meter'}).find('span', {'class':'superPageFontColor', 'style':'vertical-align:top'}).contents[0][:-1]
            int_res=soup.find('div', {'class' : 'audience-info hidden-xs superPageFontColor'}).findAll('div')
            for item in int_res:
                if ctr==1:
                    self.audience_average_rating=float(item.contents[-1].strip().split('/')[0])
                    ctr+=1
                elif ctr==2:
                    self.audience_user_ratings=int("".join(item.contents[-1].strip().split(',')))
                    ctr=1;

        except:
            pass

    def make_json(self):

        result = {"Tomatometer: All Critics Ratings" : self.tomatometer_all_critics_rating,
                  "Tomatometer: All Critics: Average Rating":self.tomatometer_all_average_rating,
                  "Tomatometer: All Critics: Reviews Counted":self.tomatometer_all_reviews_counted,
                  "Tomatometer: All Critics: Fresh":self.tomatometer_all_fresh,
                  "Tomatometer: All Critics: Rotten":self.tomatometer_all_rotten,
                  "Tomatometer: Top Critics Ratings" : self.tomatometer_top_critics_rating,
                  "Tomatometer: Top Critics: Average Rating":self.tomatometer_top_average_rating,
                  "Tomatometer: Top Critics: Reviews Counted":self.tomatometer_top_reviews_counted,
                  "Tomatometer: Top Critics: Fresh":self.tomatometer_top_fresh,
                  "Tomatometer: Top Critics: Rotten":self.tomatometer_top_rotten,
                  "Audience Score":self.audience,
                  "Audience Average Rating":self.audience_average_rating,
                  "Audience User Ratings":self.audience_user_ratings,
                  "Movie":self.title,
                  "Year":self.year}

        return json.dumps(result, indent=4, sort_keys=True)



if __name__ == "__main__":
    print('Running')
    
