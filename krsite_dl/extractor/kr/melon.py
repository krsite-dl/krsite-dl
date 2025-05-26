"""Extractor for https://melon.com"""

from utils.core import (
    Requests, 
    Logger, 
    Site,
    DataPayload,
    re,
    )

SITE_INFO = Site(hostname="melon.com", name="Melon")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    img_list = []
    artist_id = re.search(r'(?<=artistId=)\d+', hd).group(0)

    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()

    init_url = f'https://www.melon.com/artist/photoPaging.htm?startIndex=1&pageSize=5000&orderBy=NEW&listType=0&artistId={artist_id}'

    soup = site_parser._parse(site_req.session.get(init_url).text)

    photo_list = soup.find('div', class_='photo_list')

    for item in photo_list.findAll('img'):
        img_list.append(re.sub(r'(_\d+)(?=\.jpg)', '_org',
                        re.sub(r'(?<=.jpg).*$', '', item['src'])))

    site_req.session.close()
    logger.log_extractor_info(post_title, img_list)

    dir = [SITE_INFO.name, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    yield payload
