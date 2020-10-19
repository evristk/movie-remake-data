import requests
from bs4 import BeautifulSoup
import os
import html_movie_extractor as extractor
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Moviecable import MoviePair

wiki_urls = ['https://en.wikipedia.org/wiki/List_of_film_remakes_(A%E2%80%93M)',
             'https://en.wikipedia.org/wiki/List_of_film_remakes_(N%E2%80%93Z)']

html = ''
fpath = os.path.join(os.getcwd(), 'wiki_movie_remake_data.txt')

try:
    with open(fpath, 'r') as f:
        html = f.read()
except FileNotFoundError:
    html_to_str = ''
    for url in wiki_urls:
        r = requests.get(url)
        html = r.text.encode('utf8').decode('ascii', 'ignore')
        # parse with BeautifulSoup to isolate tables with movies only
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table')
        tables = tables[1:]
        # store html tables locally to avoid doing GET requests
        html_to_str = html_to_str + str(tables)

    f = open(fpath, 'w')
    f.write(html_to_str)
    f.close()

# All tables with movies
soup = BeautifulSoup(html, 'lxml')
tables = soup.find_all('table')

movie_pairs = []

# Skip first table because it does not contain any movies
for table in tables[1:]:
    rows = table.find_all('tr')
    # Skip header row
    for tr in rows[1:]:
        td_tags = tr.find_all('td')
        # Movies in column 1
        original_movie = extractor.extract_movie_data(td_tags[0])
        original_movie = original_movie[0]
        # Movies in column 2
        remade_movies = extractor.extract_movie_data(td_tags[1])
        for remade_movie in remade_movies:
            movie_pairs.append(MoviePair(original_movie, remade_movie))

# for movie_pair in movie_pairs:
#     print("%s, %s" % (movie_pair.get_original(), movie_pair.get_remake()))

# compute year difference between an original an a remake

all_remakes = pd.DataFrame.from_records([p.to_dict() for p in movie_pairs])
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)

df = all_remakes
df = df.convert_dtypes()
df['original_year'] = pd.to_numeric(df['original_year'])
df['remake_year'] = pd.to_numeric(df['remake_year'])

# useful methods for getting a better understanding of the dataset
# df.describe(), df['column_name'].describe(), df.corr()

# Generate a new column: difference in years between a remake and the original movie
df['diff_years'] = df['remake_year'].sub(df['original_year'])

# Find original movie with largest diff between its original publish and its remake publish
print(df.iloc[df['diff_years'].idxmax()])

# Since an original movie may have more than one remakes,
# we want to keep only the data about the first remake.
# So let's remove duplicate rows based on the Series 'original_year'
first_remake = df.drop_duplicates(subset=['original_title'])
df = first_remake

# Display the cumulative distribution of the difference in years between original & first remake
kwargs = {'cumulative': True}
sns.distplot(df['diff_years'], hist_kws=kwargs, kde_kws=kwargs)
plt.show()




