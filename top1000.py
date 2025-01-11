import requests
import polars as pl
from bs4 import BeautifulSoup

ranks = []
ids = []
names = []
years = []

for page in range(10):
    url = f'https://boardgamegeek.com/browse/boardgame/page/{page+1}?sort=rank'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    for row in soup("tr"):
        if rank := row.find('td', class_='collection_rank'):
            link = row.find('a', class_='primary')
            year = row.find('span', class_='smallerfont')
            ranks.append(int(rank.text))
            names.append(link.text.strip())
            ids.append(int(link['href'].split('/')[2]))
            years.append(year.text[1:-1])

print(len(ranks), len(names), len(ids), len(years))

df = pl.DataFrame({
    'rank': ranks,
    'name': names,
    'id': ids,
    'year': years
})

df.write_csv('data/top1000.csv')
