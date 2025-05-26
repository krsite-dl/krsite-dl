"""Extractor for https://news.naver.com"""

from utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="news.naver.com", name="Naver News")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('span', class_='_ARTICLE_DATE_TIME')[
        'data-date-time'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    article = soup.find('div', class_='newsct_article')

    img_list = []
    for item in article.findAll('img'):
        img_list.append(item.get('data-src').split('?')[0])

    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]
    
    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    yield payload
