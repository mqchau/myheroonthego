import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse
from common import *

from HTMLParser import HTMLParser

#PUBLIC: get a list of all movies by page number
def get_movie_list(page=1):
	r = requests.get('http://myhero.com/films/all.asp', params={'p':page})
	return extract_movie_list(r.text)

def extract_movie_list(html_string):
	soup = BeautifulSoup(html_string)
	all_movies = soup.find_all('table', id='heroHolder')
		
	return map(extract_many_movie_info, all_movies)

def extract_many_movie_info(movie):
	dict1 = extract_name_caption(movie)
	dict2 = extract_link(movie)
	return dict(dict1.items() + dict2.items())

def extract_name_caption(movie):
	spans = movie.find_all('span')
	name = ''; caption = ''
	for span in spans:
		if span['class'] == 'heroName':	
			name = span.contents[0].__str__().strip()
		elif span['class'] == 'heroCap':
			caption = strip_tags(span.__str__()).strip()
	return {'name' : name 
		,'caption': caption 
		}

def extract_link(x):
	return {
		'imglink' : DEFAULT_IMG_PREFIX + x.find('img')['src'] if x.find('img') is not None else '' 
		,'movielink' : strip_movie_link(x.find('a')['href']) if x.find('a') is not None else ''
		}

def strip_movie_link(orig):
	m = re.search("film=(.+)&res=", orig)
	if m is None:
		print orig
		return orig
	else:
		return m.group(1)

#PUBLIC: get detail of a movie
def get_movie(movie_name):
	r = requests.get('http://myhero.com/films/view.asp', params={'film':movie_name})
	return extract_movie_info(r.text)

def extract_movie_info(html_string):
	soup = BeautifulSoup(html_string)
	if soup.find('source') is None:
		return {}
	title = ''; author = '';
	spans = soup.find_all('span')
	for span in spans:
		if 'class' in span.attrs:
			if span['class'] == 'filmTitle':
				title = strip_tags(span.__str__()).strip()
			elif span['class'] == 'filmAuthor':
				author = strip_tags(span.__str__()).strip()
		else:
			print span
	return {
		'movielink': soup.find('source')['src']
		,'overview': strip_tags(soup.find('div', id='overview').__str__()).strip() 
		,'moreinfo': strip_tags(soup.find('div', id='info').__str__()).strip() 
		,'bios': strip_tags(soup.find('div', id='bios').__str__()).strip() 
		,'title': title
		,'author': remove_non_ascii(author )
	}
	
if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=3)
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", required=True, help="Debug option")

	args = parser.parse_args()

	if "debug" in args:
		if int(args.debug) == 0:
			#get the list all movies by page number
			movie_list = get_movie_list(1)
			pp.pprint(movie_list)
		elif int(args.debug) == 1:
			#get the detail of a movie
			movie = get_movie('sulai')
			pp.pprint(movie)

