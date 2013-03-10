import sys
from bs4 import BeautifulSoup as Soup

def parseLog(file):
    file = 'Dictionary.xml'
    handler = open(file).read()
    soup = Soup(handler)
    for message in soup.dictmap.findAll('lexelt'):
        if 'argument' in message['item']:
            for s in message.findAll('sense'):
                print(s['gloss'])
        '''if 'activate' in soup.lexelt.get('item'):
            print soup.lexelt.findAll('senses')'''
if __name__ == "__main__":
    parseLog('')