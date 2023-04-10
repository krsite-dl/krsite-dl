import requests
import re
from bs4 import BeautifulSoup
import down.directory as dir

def from_imbcnews(hd):
    print("Url: %s" % hd)
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_title = soup.find('h2').text
    post_date = soup.find('span', class_='date').text.strip()
    post_date_short = post_date.replace('-', '')
    img_list = []

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    for item in soup.findAll('img'):
        if item.get('src') is not None:
            if 'talkimg.imbc.com' in item.get('src'):
                img_list.append('http:' + item.get('src'))
    
    print("Found %s image(s)" % len(img_list))

    post_date = re.sub('[\u3131-\uD7A3]+', '', post_date)
    post_date = re.sub(r'\s+', ' ', post_date)
    post_date = post_date[:18].replace('-', '')

    post_date_short = re.sub('[\u3131-\uD7A3]+', '', post_date_short)[:8]

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)