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
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d')
    post_date_short = post_date.strftime('%y%m%d')

    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date_short)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)