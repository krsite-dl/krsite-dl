"""Extractor for https://osen.co.kr"""

from utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname=["osen.mt.co.kr", "osen.co.kr"], name="OSEN")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    wrap = soup.find('div', class_='detailTitle')

    post_title = wrap.find('h1').text
    post_date = soup.find('div', class_='detailTitle__post-infos').text.strip()

    img_list = []

    for item in soup.findAll('img', class_='view_photo'):
        img_list.append('https:' + item['src'].split(':')[1])

    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    post_date_short = post_date.strftime('%Y%m%d')[2:]

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
