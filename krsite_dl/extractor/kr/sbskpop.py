"""Extractor for https://sbskpop.kr"""

from utils.core import (
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="sbskpop.kr", name="SBS KPOP")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:description')[
        'content'].strip()
    post_date = datetime.datetime.strptime(post_title[:8], '%y.%m.%d')
    post_date_short = post_date.strftime('%Y%m%d')[2:]

    content = soup.find('div', class_='page-content')

    img_list = []

    for img in content.findAll('img'):
        srcset_attrs = ['data-srcset', 'srcset']
        for srcset_attr in srcset_attrs:
            srcset_value = img.get(srcset_attr)
            if srcset_value:
                sources = srcset_value.split(',')
                if sources and sources[-1] == '':
                    sources.pop()
                max_source = max(
                    sources,
                    key=lambda s: int(s.strip().split(' ')[-1][:-1]), default=None
                )
                if max_source:
                    highest_width_url = max_source.strip().split(' ')[0]
                    if highest_width_url:
                        img_list.append(highest_width_url)

    site_req.session.close()
    logger.log_extractor_info(post_title, post_date, img_list)

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers={'Referer': 'https://sbskpop.kr'}
    )

    yield payload
