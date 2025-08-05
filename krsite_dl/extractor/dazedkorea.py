"""Extractor for https://dazedkorea.com"""

from ..utils.core import (
    Requests, 
    SiteParser,
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="dazedkorea.com", name="Dazed Korea")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('h1', class_='title').text.strip()
    post_summary = soup.find('h2', class_='summary').text.strip()
    post_title = post_title + ' ' + post_summary
    post_date = soup.find('time', class_='timestamp').text.strip()
    post_date_short = post_date.replace('/', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y/%m/%d')
    content = soup.find('div', class_='article-body')

    img_list = []

    for item in content.findAll('img'):
        img_list.append('http://dazedkorea.com' + item.get('src'))

    site_req.session.close()
    logger.log_extractor_info(
        f"Summary: {post_summary}",
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
