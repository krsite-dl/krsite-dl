import requests
import datetime
from bs4 import BeautifulSoup
import down.directory as dir

def from_newsjamm(hd):
    print("Url: %s" % hd)
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_title = soup.find('h1').text
    post_date = soup.find('span', class_='PostContent_statusItem__AgJEE').text.strip()
    post_date_short = post_date.replace('.', '')
    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))

    print("Found %s image(s)" % len(img_list))

    post_date = post_date.replace('.', '')[2:]
    post_date = post_date.datetime.strftime('%y%m%d')

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)