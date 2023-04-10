import requests
from bs4 import BeautifulSoup
import down.directory as dir

def from_osen(hd):
    print("Url: %s" % hd)
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    wrap = soup.find('div', class_='detailTitle')
    post_title = wrap.find('h1').text
    post_date = soup.find('div', class_='detailTitle__post-infos').string.replace('-', '')[:8]
    img_list = []

    for item in soup.findAll('img', class_='view_photo'):
        img_list.append(item.get('src'))

    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list, post_title, post_date)