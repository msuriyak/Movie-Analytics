from __future__ import division
import urllib
from bs4 import BeautifulSoup as bs
import re
import json

class movie(object):
	def __init__(self, name, year, winner, nominee):
		self.name = name
		self.winner = winner
		self.nominee = nominee
		self.year = year

	def make_json(self):
		result = {'Name'    : self.name,
				  'Year'    : self.year,
				  'Nominee' : self.nominee,
				  'Winner'  : self.winner}
		return json.dumps(result, indent=4, sort_keys=True)

def get_all_oscar_movies():
	url = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'

	html = urllib.request.urlopen(url, timeout=2)
	soup = bs(html, 'html.parser')

	movie_list = []

	tables = soup.findAll('table', {'class' : 'wikitable'})

	for table in tables:
		year = int(table.find('big').find('a').text)
		for row in table.findAll('tr'):
			nominee = 1
			winner = 0
			if row.get('style') == 'background:#bebebe' :
				continue
			if row.get('style') == 'background:#FAEB86' :
				name = row.find('a').text 
				winner = 1
			else :
				name = row.find('a').text

			movie_json = movie(name, year, winner, nominee).make_json()
			movie_list.append(movie_json)

	return movie_list

if __name__ == '__main__' :
	for item in get_all_oscar_movies():
		item = json.loads(item)
		if item['Winner'] == 1:
			print(item)






			
