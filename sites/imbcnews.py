import requests
from bs4 import BeautifulSoup
from down.directory import dir_handler

def from_imbcnews(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_title = soup.find('h2').text
    post_date = soup.find('span', class_='date').string.replace('-', '')[:8]
    img_list = []

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    for item in soup.findAll('img'):
        if item.get('src') is not None:
            if 'talkimg.imbc.com' in item.get('src'):
                img_list.append('http:' + item.get('src'))
    
    print("Found %s image(s)" % len(img_list))
    dir_handler(img_list, post_title, post_date)