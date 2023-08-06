import requests
from bs4 import BeautifulSoup
import re
import unidecode

__all__ = ["synonymo", "linternaute", "larousse", "cnrtl"]

def _synonymo(mot):    
    r = requests.get(f"http://www.synonymo.fr/synonyme/{mot}")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find_all('a', {'class': 'word', 'title': re.compile('.+')})
    if words == None:
        return ()
    for word in words:
        yield word.text.strip()

def _linternaute(mot):
    # retirer les accents
    mot = unidecode.unidecode(mot).replace(' ', '-')
    r = requests.get(f"https://www.linternaute.fr/dictionnaire/fr/synonyme/{mot}")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find('ul', {'class': 'dico_liste grid_line'})
    if words == None:
        return ()
    words = words.findChildren('a')
    for word in words:
        yield word.text.strip()

def _larousse(mot):    
    # retirer les accents
    mot = unidecode.unidecode(mot)
    r = requests.get(f"https://www.larousse.fr/dictionnaires/francais/{mot}/#synonyme", allow_redirects=True)
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    synonyms_headers = bs.find_all('p', string='Synonymes :')
    if synonyms_headers == None:
        return ()
    for header in synonyms_headers:
       for word in header.find_next('li').text.split('-'):
            yield word.strip()

def _cnrtl(mot):
    r = requests.get(f"https://cnrtl.fr/synonymie/{mot}//1?ajax=true#")
    r.encoding = r.apparent_encoding
    bs = BeautifulSoup(r.text, 'html.parser')
    words = bs.find_all('td', {'class': 'syno_format'})
    if words == None:
        return ()
    for word in words:
        yield word.findChildren('a')[0].text.strip()


def synonymo(mot):
    return  list(_synonymo(mot))

def linternaute(mot):
    return  list(_linternaute(mot))

def larousse(mot):
    return  list(_larousse(mot))

def cnrtl(mot):
    return  list(_cnrtl(mot))
