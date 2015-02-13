import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def save_html(file_name, html_string):
	with open(file_name + ".html", "w") as f:
		f.write(html_string.encode('utf8'))
		
def get_story_in_type(type_link):
	r = requests.get('http://myhero.com/directory/' + type_link)
	return extract_story_info(r.text)

def extract_story_info(html_string):
	soup = BeautifulSoup(html_string)
	all_herotext = soup.find_all('div', id='heroText')
	all_td_herotext = map(lambda x: x.parent, all_herotext)
	all_story_info = map(lambda x: {
		'imglink' : x.find('img')['src'] if x.find('img') is not None else '' 
		,'storylink' : x.find('a')['href']
		,'name' : strip_tags(x.find('strong').__str__())
		,'description': x.find('font').contents[0] if len(x.find('font').contents) > 0 else ''
		}, all_td_herotext)
	return all_story_info 

def get_story_type_description():
	r = requests.get('http://myhero.com/directory')
	soup = BeautifulSoup(r.text)
	all_essayttl = soup.find_all("essayttl")
	all_essayttl_parent = map(lambda x: x.parent, all_essayttl)
	all_essayttl_profile = map(extract_type_description, all_essayttl_parent)
	return all_essayttl_profile

def extract_type_description(x):
	return {
		"type": x.find("essayttl").contents[0]
		,"description": x.contents[-1].strip()
		,"tag": x['href'] 
		}


if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=3)
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", required=True, help="Debug option")

	args = parser.parse_args()

	if "debug" in args:
		if int(args.debug) == 0:
			#do http get of list of stories type
			r = requests.get('http://myhero.com/directory')
			print type(r.text)
			with open("story_types.html", "w") as f:
				f.write(r.text.encode('utf8'))
		elif int(args.debug) == 1:
			#get all types of stories and their descriptions 
			all_story_type_description = get_story_type_description()
			pp.pprint(all_story_type_description)
		elif int(args.debug) == 2:
			#get all stories of a specific type, let's test with aids
			all_stories = get_story_in_type('page.asp?dir=aids')
			pp.pprint(all_stories)
		elif int(args.debug) == 3:
			#extract info from stories page
			with open("aids_stories.html", 'r') as f:
				html_string = f.read()
			all_stories = extract_story_info(html_string)
			pp.pprint(all_stories)
		elif int(args.debug) == 4:
			#get all stories of a specific type, let's test with women 
			all_stories = get_story_in_type('page.asp?dir=women')
			pp.pprint(all_stories)
