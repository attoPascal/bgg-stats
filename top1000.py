import requests
import polars as pl
from bs4 import BeautifulSoup

ranks = []
ids = []
names = []

for page in range(10):
    url = f'https://boardgamegeek.com/browse/boardgame/page/{page+1}?sort=rank'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='lxml')

    for row in soup("tr"):
        if rank := row.find('td', 'collection_rank'):
            link = row.find('a', 'primary')
            year = row.find('span', 'smallerfont')
            ranks.append(int(rank.text))
            names.append(link.text.strip())
            ids.append(int(link['href'].split('/')[2]))

print(len(ranks), len(names), len(ids))

df = pl.DataFrame({
    'rank': ranks,
    'name': names,
    'id': ids
})

df.write_csv('data/top1000.csv')
