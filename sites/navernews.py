import requests
from bs4 import BeautifulSoup
import down.directory as dir


def from_navernews(hd):
    print("Url: %s" % hd)
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    post_title = soup.find('h2', class_='end_tit').text.strip()
    post_date = soup.find('span', class_='author').text.strip()[4:15].replace('.', '')
    img_list = [] 

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    article = soup.find('div', class_='end_ct_area')

    for item in article.findAll('img'):
        if 'upload' not in item.get('src'):
            img_list.append(item.get('src').split('?')[0])

    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list, post_title, post_date)