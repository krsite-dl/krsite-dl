"""Extractor for https://tvreport.co.kr"""

from ..utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="tvreport.co.kr", name="TV Report")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    img_list = []

    post_title = soup.find('h1', class_='entry-title').text.strip()
    post_date = soup.find('time').text.strip()

    for i in soup.find_all('p', class_='dp-image-container'):
        img_list.append(i.find('img')['src'])

    post_date = re.sub('[\u3131-\uD7A3]+|\s+', '', post_date)
    post_date = post_date + ' ' + '00:00:00'
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

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
