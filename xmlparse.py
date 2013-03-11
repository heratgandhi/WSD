import sys
import re
from bs4 import BeautifulSoup as Soup

def parseLog(file):
    file = 'Dictionary.xml'
    content = open(file).read()
    main_str = re.compile('<lexelt item="argument.[a-z]">(.*?)</lexelt>', re.DOTALL |  re.IGNORECASE).findall(content)[0]
    return re.compile('gloss="(.*)"').findall(main_str)
    
if __name__ == "__main__":
    parseLog('')