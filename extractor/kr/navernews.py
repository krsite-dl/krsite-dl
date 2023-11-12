import requests
import datetime

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="news.naver.com", name="Naver News", location="KR")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')
    
    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('span', class_='_ARTICLE_DATE_TIME')['data-date-time'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    article = soup.find('div', class_='newsct_article')
    
    img_list = []
    for item in article.findAll('img'):
        # print(item)
        img_list.append(item.get('data-src').split('?')[0])

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