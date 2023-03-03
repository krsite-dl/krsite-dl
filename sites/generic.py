import requests
from bs4 import BeautifulSoup
import down.directory as dir

def from_generic(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))
    
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list)