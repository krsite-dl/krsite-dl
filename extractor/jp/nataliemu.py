import requests
from bs4 import BeautifulSoup

def from_nataliemu(hd):
    r = requests.get(hd)

    soup = BeautifulSoup(r.text, 'html.parser')

    content = soup.find('article')
    post_title = content.find('h1', class_='NA_article_title').text
    post_date = content.find('span', class_='NA_article_date').text

    