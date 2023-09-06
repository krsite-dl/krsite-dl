import requests
import datetime
from pytz import timezone
from bs4 import BeautifulSoup
import down.directory as dir

def from_topstarnews(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_dates = soup.find_all('meta', property='article:published_time')
    if len(post_dates) >= 2:
        post_date = post_dates[1].attrs['content']
    else:
        post_date = post_dates[0].attrs['content']

    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)
    
    img_list = []

    content = soup.find('div', itemprop='articleBody')

    for item in content.findAll('img'):
        img_list.append(item.get('data-org'))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_no_folder(img_list, post_title, post_date_short, post_date, loc, folder_name)