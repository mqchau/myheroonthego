import re
import pprint
import requests
from bs4 import BeautifulSoup
import argparse
from common import *

from HTMLParser import HTMLParser

		
#PUBLIC: show what stories in a category based on the tag
def get_story_in_type(type_link):
	r = requests.get('http://myhero.com/directory/page.asp?dir=' + type_link)
	return extract_story_info(r.text)

def extract_story_info(html_string):
	soup = BeautifulSoup(html_string)
	all_herotext = soup.find_all('div', id='heroText')
	all_td_herotext = map(lambda x: x.parent, all_herotext)
	all_story_info = map(lambda x: {
		'imglink' : DEFAULT_IMG_PREFIX + x.find('img')['src'] if x.find('img') is not None else '' 
		,'storylink' : strip_story_link(x.find('a')['href'])
		,'name' : strip_tags(x.find('strong').__str__())
		,'description': x.find('font').contents[0] if len(x.find('font').contents) > 0 else ''
		}, all_td_herotext)
	return all_story_info 

def strip_story_link(orig):
	m = re.search("hero=(.+)$", orig)
	if m is None:
		print orig
		return orig
	else:
		return m.group(1)

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
	r = requests.get("http://myhero.com/hero.asp?hero=" + story_link)
	return extract_story_content(r.text)
 
def extract_story_content(html_string):
	soup = BeautifulSoup(html_string)
	#find the title
	title_area = soup.find('div', id='titleArea')
	heroCat = ''; nameCat = ''; authorCat = '';
	for i in title_area.find_all('div'):
		#print str(i) + "  " + str(i.attrs['class'])
		if 'heroCat' in i['class']:
			heroCat = i.contents[0]
		elif 'nameCat' in i['class']:
			nameCat = i.contents[0]
		elif 'authorCat' in i['class']:
			authorCat = i.contents[0]
	#find the content
	main_content = None
	for i in soup.find_all('center'):
		if i.find('table') is not None:
			main_content = i
	if main_content is None:
		return {}
	pp.pprint(main_content)
	table = main_content 
	all_content = decode_story_content_td(table)
	return {
		'heroCat': heroCat,
		'nameCat': nameCat,
		'authorCat': authorCat,
		'content' : all_content
		}

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
		if int(args.debug) == 1:
			#get all types of stories and their descriptions 
			all_story_type_description = get_story_type_description()
			pp.pprint(all_story_type_description)
		elif int(args.debug) == 2:
			#get all stories of a specific type, let's test with aids
			all_stories = get_story_in_type('aids')
			pp.pprint(all_stories)
		elif int(args.debug) == 4:
			#get all stories of a specific type, let's test with women 
			all_stories = get_story_in_type('women')
			pp.pprint(all_stories)
		elif int(args.debug) == 5:
			#get story content of a specific hero
			story_content = get_story_content('kofi_annan')
			pp.pprint(story_content)
	
