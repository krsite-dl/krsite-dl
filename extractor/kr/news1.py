import requests
import datetime

from pytz import timezone
from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="news1.kr", name="News1", location="KR")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
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

    DirectoryHandler().handle_directory_combine(payload)