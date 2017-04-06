from __future__ import division
import urllib
from bs4 import BeautifulSoup as bs
import re
import json

class metacritic(object):
    def __init__(self, title='', year=''):
        self.query_title = title
        self.query_en = year

    def collect_data(self, title, year):
        url = 'http://www.metacritic.com/movie/'
        title = title.lower().replace(' ', '-')
        url_choices = [title, title + '-' + str(year)]
        print(title)
        print(url_choices)
        try :
            print(url + url_choices[0])
            html = urllib.request.urlopen(url + url_choices[0])
            print('Success')
        except :
            print(url + url_choices[1])
            html = urllib.request.urlopen(url + url_choices[1])
            print('Error')
        '''
        page_request = urllib2.Request(url,headers = hdr)
        test_page = urllib2.urlopen(page_request)
        souped_up = BeautifulSoup(test_page,'lxml')
        #print souped_up.title
        meta_100 = souped_up.find("span", class_="metascore_w header_size movie positive perfect")
        meta_pos = souped_up.find("span", class_="metascore_w header_size movie positive")
        meta_mix = souped_up.find("span", class_="metascore_w header_size movie mixed")
        meta_neg = souped_up.find("span", class_="metascore_w header_size movie negative")
        meta_tbd = souped_up.find("span", class_="metascore_w header_size movie tbd")
        if(meta_100):
            metascore = int(meta_100.text)
        if (meta_pos):
            metascore = int(meta_pos.text)
            #print metascore
        if (meta_mix):
            metascore = int(meta_mix.text)
        if (meta_neg):
            metascore = int(meta_neg.text)
        if(meta_tbd):
            metascore = 200
        return metascore
        '''
if __name__ == '__main__':
    print('Running main!!!')
    temp = metacritic()
    temp.collect_data('logan', 2017)
    temp.collect_data('la la land', 2016)
