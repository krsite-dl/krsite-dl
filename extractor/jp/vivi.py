import requests
import datetime

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from rich import print
from pytz import timezone
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="vivi.tv", name="Vivi", location="JP")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    article = soup.find('article', class_='single-post')

    img_list = []
    for img in article.find_all('img'):
        if img.has_attr('data-src'):
            img_list.append(f"https://{img['data-src'].split('//')[-1]}")

    
    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found: %s image(s)" % len(img_list))

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