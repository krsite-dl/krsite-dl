"""Extractor for https://isplus.com"""

from ..utils.core import (
    urlparse,
    timezone,
    Requests,
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="isplus.com", name="Ilgan Sports")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    host = f"{urlparse(hd).scheme}://{urlparse(hd).netloc}"
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content']
    post_date = soup.find('meta', property='article:modified_time')['content']
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='article_body')

    img_list = []

    for img in content.findAll('img'):
        if img.get('src'):
            img = re.sub(re.compile(r'\.\d+x\.\d+'), '', img.get('src'))
            img_list.append(f"{host}{img}")

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
