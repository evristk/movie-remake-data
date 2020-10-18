import requests
from bs4 import BeautifulSoup
import os
import html_movie_extractor as extractor

wiki_url = 'https://en.wikipedia.org/wiki/List_of_film_remakes_(A%E2%80%93M)'
html = ''
fpath = os.path.join(os.getcwd(), 'a_m.txt')

try:
    with open(fpath, 'r') as f:
        html = f.read()
except FileNotFoundError:
    r = requests.get(wiki_url)
    html = r.text.encode('utf8').decode('ascii', 'ignore')
    f = open(fpath, 'w')
    f.write(html)
    f.close()

soup = BeautifulSoup(html, 'lxml')
tables = soup.find_all('table')

list_tr = tables[1].find_all('tr')

# Skip header row
for tr in list_tr[1:]:
    td_tags = tr.find_all('td')
    # Movies in column 1
    extractor.get_movie_titles(td_tags[0])
    # Movies in column 2
    extractor.get_movie_titles(td_tags[1])

# print("Number of tables retrieved: %d" % len(tables))
