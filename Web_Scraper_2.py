# URL of Web Page : https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
from random import randint
from time import sleep

# Initialize empty lists where you'll store your data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

# Making sure we get English Translated titles from the movies we scrape
headers = {"Accept-Language" : "en-US, en;q=0.5"}

# When we go to the next page the start value changes by 50
pages = np.arange(1, 1001, 50)

for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start="+str(page)+"&ref_=adv_prv")
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    # To control the crawl rate
    sleep(randint(2, 10))
    for container in movie_div:
        name = container.h3.a.text
        titles.append(name)

        year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
        years.append(year)

        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)

        rating = float(container.strong.text)
        imdb_ratings.append(rating)

        meta = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(meta)

        nv = container.find_all('span', attrs = {'name':'nv'})
        vote = nv[0].text
        votes.append(vote)

        gross = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(gross)

movies = pd.DataFrame({
'Movie': titles,
'Year': years,
'Time Duration': time,
'Rating': imdb_ratings,
'Meta Score': metascores,
'Votes': votes,
'Gross Income (in Millions)': us_gross,
})

# Data Cleaning
movies["Movie"] = movies["Movie"].map(lambda x : x.strip())

movies["Year"] = movies["Year"].str.extract('(\\d+)').astype(int)

movies["Time Duration"] = movies["Time Duration"].str.extract('(\\d+)')
movies["Time Duration"] = pd.to_numeric(movies["Time Duration"], errors='coerce')

movies["Votes"] = movies["Votes"].str.replace(',','').astype(int)

movies["Meta Score"] = movies["Meta Score"].str.extract('(\\d+)')
movies["Meta Score"] = pd.to_numeric(movies["Meta Score"], errors='coerce')

movies["Gross Income (in Millions)"] = movies["Gross Income (in Millions)"].map(lambda x : x.lstrip('$').rstrip('M'))
movies["Gross Income (in Millions)"] = pd.to_numeric(movies["Gross Income (in Millions)"], errors='coerce')

movies.to_csv("movies.csv")