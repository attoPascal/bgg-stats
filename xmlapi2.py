import requests
from bs4 import BeautifulSoup, Tag

class Thing:
    def __init__(self, id_):
        self.url = f'https://boardgamegeek.com/xmlapi2/thing?id={id_}'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, features='xml')
    
    def value(self, name):
        soup = self.soup.find(name)
        if isinstance(soup, Tag) and soup.has_attr('value'):
            return soup['value']
    
    def number(self, name):
        value = self.value(name)
        if isinstance(value, str):
            try:
                return int(value)
            except:
                return 0
        return 0
    
    def string(self, name):
        value = self.value(name)
        if isinstance(value, str):
            return value
        return ""
    
if __name__ == '__main__':
    game = Thing(240980)
    print(f"{game.string('name')} ({game.number('yearpublished')})")
