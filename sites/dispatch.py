import requests
import re
from bs4 import BeautifulSoup
import down.directory as dir
def from_dispatch(hd):
    print("Url: %s" % hd)
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []
    post_date = soup.find('div', class_='post-date').text.strip()
    post_title = soup.find('div', class_='page-post-title').string.strip()
    post_date_short = post_date.replace('.', '')[:8]

    for i in soup.findAll('img', class_='post-image'):
        if i.get('data-src') != None:
            temp = i.get('data-src')
            img_list.append(temp)
        else:
            temp = i.get('src')
            img_list.append(temp)
    
    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    post_date = post_date[:18].replace('.', '')
    post_date = re.sub('[\u3131-\uD7A3]+', '', post_date)
    post_date = re.sub(r'\s+', ' ', post_date)
    
    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)