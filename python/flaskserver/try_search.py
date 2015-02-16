import requests
from common import *

payload = {'keyword': 'black', 'area': 'art', 'criteria': 'key', 'specificarea':'chkArt', 'submit': 'Search'}
payload2 = {'keyword': 'black', 'button': 'Search', 'area': 'art'}
r  = requests.post('http://myhero.com/search/index.asp', data=payload2)

save_html('try_search', r.text)
