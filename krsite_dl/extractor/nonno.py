"""Extractor for https://nonno.hpplus.jp"""

from ..utils.core import (
    timezone,
    urlparse,
    urlunparse,
    Requests, 
    SiteParser,
    Logger, 
    Site,
    DataPayload,
    re,
    json,
    datetime, 
    )


SITE_INFO = Site(hostname="nonno.hpplus.jp", name="Non-no")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    # article info
    info = (soup.find_all('script', type='application/ld+json')[2])
    info = json.loads(info.string)

    post_title = info['headline']
    post_date = datetime.datetime.strptime(
        info['datePublished'], '%Y-%m-%dT%H:%M:%S%z')
    post_date_short = post_date.strftime('%y%m%d')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    contents = soup.find_all('figure')

    img_list = []
    for content in contents:
        img = content.find('img')
        url_parts = urlparse(img['src'])
        new_url_parts = url_parts._replace(query=None, path=re.sub(
            r'/q=\d+,\w+=\w+:\w+', '', url_parts.path))
        img_url = urlunparse(new_url_parts)
        img_list.append(img_url)

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
