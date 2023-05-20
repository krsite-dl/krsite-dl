import requests
import datetime
from pytz import timezone
import json
from bs4 import BeautifulSoup
import down.directory as dir

def from_lofficielkorea(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    script_tag = soup.find('script', type='application/ld+json')
    json_data = json.loads(script_tag.string)

    post_title = json_data['headline']
    post_date = json_data['datePublished']
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('section', class_='article-layout__main')
    for item in content.findAll('img'):
        print(item.get('src'))



    print("Title: %s" % post_title)
    print("Date: %s" % post_date)