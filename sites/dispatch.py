import requests
from bs4 import BeautifulSoup
from down.directory import dir_handler_alt

def from_dispatch(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []
    post_date = soup.find('div', class_='post-date').string.replace('.', '').strip()[:8]
    post_title = soup.find('div', class_='page-post-title').string.strip()

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
    
    dir_handler_alt(img_list, post_title, post_date)