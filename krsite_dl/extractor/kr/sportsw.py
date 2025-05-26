"""Extractor for https://sportsw.kr"""

from utils.core import (
    timezone,
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="sportsw.kr", name="SportsW")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='viewConts')

    img_list = []
    for img in content.findAll('img'):
        img_list.append('https://sportsw.kr' +
                        img.get('src').replace('_thum', ''))

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
