import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse

def save_html(file_name, html_string):
	with open(file_name + ".html", "w") as f:
		f.write(html_string.encode('utf8'))
		
def get_story_in_type(type_link):
	r = requests.get('http://myhero.com/directory/' + type_link)
	soup = BeautifulSoup(r.text)
	save_html('aids_stories', r.text)
	return None

def extract_story_info(html_string):
	soup = BeautifulSoup(html_string)
	all_herotext = soup.find_all('div', id='heroText')
	all_td_herotext = map(lambda x: x.parent, all_herotext)
	all_story_info = map(lambda x: {
		'imglink' : x.find('img') is None ? '' : x.find('img')['src']
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
		elif int(args.debug) == 4:
			#extract info from stories page
			with open("aids_stories.html", 'r') as f:
				html_string = f.read()
			all_stories = extract_story_info(html_string)
			pp.pprint(all_stories)
