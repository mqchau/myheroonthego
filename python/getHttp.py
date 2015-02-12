import requests
from bs4 import BeautifulSoup

r = requests.get('http://myhero.com/directory')
r = requests.get('http://myhero.com/directory/page.asp', params={'dir': 'lifesaver'})

soup = BeautifulSoup(r.text)
print (soup.prettify())
