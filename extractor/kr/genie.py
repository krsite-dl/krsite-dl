import requests

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup

def from_genie(hd, loc, folder_name):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})

    soup = BeautifulSoup(r.text, 'html.parser')

    print(soup.prettify())