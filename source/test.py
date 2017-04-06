from bs4 import BeautifulSoup
import urllib2
import numpy as np
general_url = "http://www.metacritic.com/movie/"
def movie (i=0,mode=0)
	names = ["La La Land",
			 "Logan 2017",
			 "Life 2017",
			 "The Godfather",
			 "Daredevil",
			 "United Passions"]
	if (mode==0):
		return names[i]
	elif (mode==1):
		return len(names)
		 
def url (i=0,mode=0):
	address = ["http://www.metacritic.com/movie/la-la-land",
			   "http://www.metacritic.com/movie/logan-2017",
			   "http://www.metacritic.com/movie/life-2017",
			   "http://www.metacritic.com/movie/the-godfather",
			   "http://www.metacritic.com/movie/daredevil",
			   "http://www.metacritic.com/movie/united-passions",]
	if (mode==0):
		return address[i]
	elif (mode==1):
		return len(address)

def metric(address):
	url = address
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
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

def main():
	scores = np.zeros(url(0,1))
	for i in range(0,url(0,1)):
		scores[i]=metric(url(i))
	print scores


main()