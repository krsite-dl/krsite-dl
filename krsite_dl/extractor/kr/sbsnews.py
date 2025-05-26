"""Extractor for https://ent.sbs.co.kr"""

from utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="ent.sbs.co.kr", name="SBS News")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('h1', class_='cth_title').text.strip()
    post_date = soup.find('span', class_='cth_text').text
    post_date = re.sub('[\u3131-\uD7A3]+', '', post_date).strip()
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d %H:%M')
    content = soup.find('div', class_='w_ctma_text')
    post_date_short = post_date.strftime('%y%m%d')
    img_list = []

    for i in content.find_all('img'):
        img_list.append(i.get('data-v-src'))

    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )

    dir = [SITE_INFO.name, post_date_short, {post_title}]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    yield payload
