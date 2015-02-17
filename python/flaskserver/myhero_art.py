import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse
from common import *

from HTMLParser import HTMLParser

#PUBLIC: get a list of art mediums
def get_art_medium_list():
	r = requests.get('http://myhero.com/gallery/browse.asp')
	return extract_art_medium(r.text)

def extract_art_medium(html_string):
	soup = BeautifulSoup(html_string)
	all_art = soup.find('div', id='galleryContainMain')
	all_td_art = all_art.find_all('td') 
	all_art_info = map(lambda x: {
		'imglink' : x.find('img')['src'] if x.find('img') is not None else '' 
		,'artlink' : strip_art_link(x.find('a')['href']) if x.find('a') is not None else ''
		,'name' : strip_tags(x.find('span').__str__())
		}, all_td_art)
	all_art_info = filter(lambda x: len(x['artlink']) > 0, all_art_info)
	return all_art_info 

def strip_art_link(orig):
	m = re.search("keyword=(.+)$", orig)
	if m is None:
		print orig
		return orig
	else:
		return m.group(1)

#PUBLIC: get a list of art in a medium type
def get_art_list(medium, page=1):
	r = requests.get('http://myhero.com/gallery/list.asp?', params={'keyword': medium, 'p' : page})
	return extract_art_list(r.text)

def extract_art_list(html_string):
	soup = BeautifulSoup(html_string)
	all_art = soup.find_all('table', id='heroHolder')
	all_art_info = map(lambda x: {
		'imglink': x.find('img')['src'] if x.find('img') is not None else '' 
		,'artlink' : x.find('a')['href'] if x.find('a') is not None else ''
		,'name': reduce(lambda x,y: (strip_tags(x.__str__()).strip() if type(x) is not str else x) + ' ' + strip_tags(y.__str__()).strip(), x.find_all('span'))
		}, all_art)
	return all_art_info

#PUBLIC: get info of a particular artwork
def get_artwork(artkey):
	r = requests.get('http://myhero.com/gallery/open.asp?', params={'art': artkey})
	return extract_artwork(r.text)

def extract_artwork(html_string):
	soup = BeautifulSoup(html_string)
	x = soup.find('div', id='artContainer')
	spans = x.find_all('span')
	title = ''; artist = ''; caption = ''; description = '';
	for span in spans:
		if span['class'] == 'gTitle':	
			title = span.contents[0].__str__().strip()
		elif span['class'] == 'gArtist':
			artist = span.contents[0].__str__().strip()
		elif span['class'] == 'gCaption':
			caption = span.contents[0].__str__().strip()
		elif span['class'] == 'gDescription':
			description = span.contents[0].__str__().strip()

	art_info = {
		'imglink': x.find('img')['src'] if x.find('img') is not None else '' 
		,'title': title, 'artist': artist, 'caption': caption, 'description': description
		} 
	return art_info

 
if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=3)
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", required=True, help="Debug option")

	args = parser.parse_args()

	if "debug" in args:
		if int(args.debug) == 0:
			#get a list of art mediums
			art_medium_list = get_art_medium_list()
			pp.pprint(art_medium_list)
		elif int(args.debug) == 1:
			#get a list of arts in a medium
			art_list = get_art_list('Digital Imagery', 2)
			pp.pprint(art_list)
		elif int(args.debug) == 2:
			#get detail of a particular artwork	
			artwork = get_artwork('nate_visualizes')
			pp.pprint(artwork)
