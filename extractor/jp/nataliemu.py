import requests
import re
import json
import datetime
from bs4 import BeautifulSoup

def from_nataliemu(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    json_raw = soup.find('script', type='application/ld+json')
    json_data = re.sub(r'\\/', '/', bytes(json_raw.string, "utf=8").decode("unicode_escape"))
    data = json.loads(json_data)

    post_title = data[0]["itemListElement"][-1]["item"]["name"]
    post_date = data[1]["datePublished"]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    post_date = post_date.replace(tzinfo=None)
    post_date_short = post_date.strftime('%Y%m%d')[2:]

    print(post_title)
    print(post_date)

    content = soup.find('div', class_='NA_article_gallery')

    img_list = []
    for item in content.findAll('img'):
        img_list.append(item['data-src'].split('?')[0])

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)