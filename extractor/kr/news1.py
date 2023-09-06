import requests
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import down.directory as dir

def from_news1(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip().encode('latin-1').decode('utf-8', 'ignore')
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)
    post_date_short = post_date.strftime('%y%m%d')

    article = soup.find('div', id='article_body_content')

    img_list = []
    for item in article.findAll('img'):
        if 'kakao' not in item['src']:
            img_list.append(item['src'].replace('article', 'original'))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_no_folder(img_list, post_title, post_date_short, post_date, loc, folder_name)