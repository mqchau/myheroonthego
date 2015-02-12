import pprint
import requests
from bs4 import BeautifulSoup
import argparse

def extract_type_description(x):
	return {
		"type": x.find("essayttl").contents[0]
		,"description": x.contents[-1].strip()
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
			#load the list of stories in html format and parse it
			with open("story_types.html", "r") as f:
				html_string = f.read()
			soup = BeautifulSoup(html_string)
		#	print (soup.prettify())
			all_essayttl = soup.find_all("essayttl")
			all_essayttl_parent = map(lambda x: x.parent, all_essayttl)
			all_essayttl_profile = map(extract_type_description, all_essayttl_parent)
			pp.pprint(all_essayttl_profile)
