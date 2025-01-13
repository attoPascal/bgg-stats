import requests
from bs4 import BeautifulSoup

class Thing:
    def __init__(self, id_):
        self.url = f'https://boardgamegeek.com/xmlapi2/thing?id={id_}'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, features='xml')
    
    def value(self, name):
        soup = self.soup.find(name)
        return soup['value']
    
    def number(self, name):
        value = self.value(name)
        return int(value)
    
    def string(self, name):
        value = self.value(name)
        return str(value)
    
if __name__ == '__main__':
    game = Thing(240980)
    print(f"{game.string('name')} ({game.number('yearpublished')})")
