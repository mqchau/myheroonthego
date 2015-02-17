import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse
from common import *

from HTMLParser import HTMLParser

DEFAULT_IMG_PREFIX = "myhero.com"
		
#PUBLIC: show what stories in a category based on the tag
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

#PUBLIC: show all stories categories and their description
def get_story_type_description():
	r = requests.get('http://myhero.com/directory')
	soup = BeautifulSoup(r.text)
	all_essayttl = soup.find_all("essayttl")
	all_essayttl_parent = map(lambda x: x.parent, all_essayttl)
	all_essayttl_parent = filter(lambda x: re.search("page\.asp", x['href']), all_essayttl_parent)
	all_essayttl_profile = map(extract_type_description, all_essayttl_parent)
	return all_essayttl_profile

def extract_type_description(x):
	return {
		"type": x.find("essayttl").contents[0]
		,"description": x.contents[-1].strip()
		,"tag": strip_story_category_link(x['href'])
		}

def strip_story_category_link(orig):
	m = re.search("dir=(.+)$", orig)
	if m is None:
		print orig
		return orig
	else:
		return m.group(1)

#PUBLIC: show the text and images in a story
def get_story_content(story_link):
	if re.search("^\.\.", story_link):
		story_link = re.sub("^\.\.", "", story_link)
	r = requests.get("http://myhero.com" + story_link)
	save_html("onehero.html", r.text)
	return extract_story_conent(r.text)
 
def extract_story_conent(html_string):
	soup = BeautifulSoup(html_string)
	table = soup.find('center').find('table').find('td')
	all_content = decode_story_content_td(table)
	#all_td = table.find_all('td')
	#all_content = []
	#for one_td_id in xrange(len(all_td)):
	#	all_content.extend(decode_story_content_td(all_td[one_td_id]))
	pp = pprint.PrettyPrinter(indent=3)
	pp.pprint(all_content)

def decode_story_content_td(td):
	#print "--------------------------------------------"
	#print type(td)
	#print td.__str__()
	single_td_content = []
	body = td.find_all(lambda x: x.name == 'img' or x.name == 'p')
	return filter(lambda y: y is not None, map(lambda x: extract_img_link(x) if x.name == 'img' else extract_p_content(x), body)) 
	#if td.find_all['img'] is not None:
	#	single_td_content.extend(map(extract_img_link, td.find_all['img']))
	#if td.find_all['p'] is not None:
	#	single_td_content.extend(map(extract_p_content, td.find_all['p']))
	return single_td_content

def extract_img_link(img_soup):
	src = DEFAULT_IMG_PREFIX + img_soup['src']
	description = None
	table_parent = filter(lambda x: x.name == 'table', img_soup.parents)
	#print img_soup
	if len(table_parent) > 0: 
		parent_table = table_parent[0]
		if parent_table.find('font') is not None:
			description = strip_tags(parent_table.find('font').__str__()).strip()
	if description is None:
		return {
			'kind': 'image',
			'link': src
		}
	else:
		return  {
			'kind': 'image',
			'link': src,
			'description': description
		}


def extract_p_content(p_soup):
	raw_content = strip_tags(p_soup.__str__()).strip()
	if len(raw_content) > 0:
		return {
			'kind': 'text',
			'text': raw_content}
	else:
		return None

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
		elif int(args.debug) == 5:
			#get story content of a specific hero
			story_content = get_story_content('../hero.asp?hero=LAKHDAR')
			pp.pprint(story_content)
		elif int(args.debug) == 6:
			#extract story content of a hero
			with open("onehero.html", 'r') as f:
				html_string = f.read()
			extract_story_conent(html_string)
