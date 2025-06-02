"""Extractor for https://marieclairekorea.com/"""

from ..utils.core import (
    timezone,
    Requests, 
    SiteParser,
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="marieclairekorea.com", name="Marie Claire Korea")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('span', class_='updated').text.strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)
    content = soup.find('div', class_='post-content')

    img_list = []

    for item in content.findAll('img'):
        img_list.append(re.sub(r'-(\d+x\d+)', '', item.get('data-orig-src')))

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
