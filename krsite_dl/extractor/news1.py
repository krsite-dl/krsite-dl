"""Extractor for https://news1.kr"""

from ..utils.core import (
    timezone,
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="news1.kr", name="News1")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')[
        'content'].strip().encode('latin-1').decode('utf-8', 'ignore')
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)
    post_date_short = post_date.strftime('%y%m%d')

    article = soup.find('div', id='article_body_content')

    img_list = []
    for item in article.findAll('img'):
        if 'kakao' not in item['src']:
            img_list.append((item['src'].replace(
                'article', 'original'), item['alt'].strip()))

    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )

    dir = [SITE_INFO.name, post_date_short]
    
    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option='combine',
        custom_headers=None
    )

    yield payload
