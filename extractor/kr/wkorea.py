import requests
import datetime
import re

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from pytz import timezone
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="wkorea.com", name="W Korea", location="KR")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    contents = soup.find('div', class_='masonry_grid')

    if contents is None:
        contents = soup.find('div', class_='post_content')

    img_list = set()
    for item in contents.findAll('img'):
        i = item.get('src')
        if i.startswith('http'):
            img_list.add(re.sub(r'-\d+x\d+', '', i))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    payload = ScrapperPayload(
        title=post_title,
        shortDate=post_date_short,
        mediaDate=post_date,
        site=SITE_INFO.name,
        series=None,
        writer=None,
        location=SITE_INFO.location,
        media=img_list,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)