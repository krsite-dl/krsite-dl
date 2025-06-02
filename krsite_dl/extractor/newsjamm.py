"""Extractor for https://newsjamm.co.kr"""

from ..utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="newsjamm.co.kr", name="Newsjamm")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find(
        'span', class_='PostContent_statusItem__AgJEE').text.strip()
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d')
    post_date_short = post_date.strftime('%y%m%d')

    content = soup.find('div', class_='PostContent_contentSection__ChFQz')

    img_list = []

    for item in content.findAll('img'):
        img_list.append(item.get('src'))

    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )

    dir = [SITE_INFO.name, post_date_short, post_title]
    
    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    yield payload
