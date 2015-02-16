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
	return extract_story_info(r.text)

def extract_story_info(html_string):
	soup = BeautifulSoup(html_string)
	all_art = soup.find('div', id='galleryContainMain')
	all_td_art = all_art.find_all('td') 
	all_art_info = map(lambda x: {
		'imglink' : x.find('img')['src'] if x.find('img') is not None else '' 
		,'artlink' : x.find('a')['href'] if x.find('a') is not None else ''
		,'name' : strip_tags(x.find('span').__str__())
		}, all_td_art)
	all_art_info = filter(lambda x: len(x['artlink']) > 0, all_art_info)
	return all_art_info 

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
