"""Extractor for https://vogue.co.kr"""

import datetime

from pytz import timezone
from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="vogue.co.kr", name="Vogue Korea")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='contt')

    # print(content)

    img_list = []

    for item in content.findAll('img'):
        if item.get('data-src') is not None:
            i = item.get('data-src')
            img_list.append(i.split('-')[0] + '.' + i.split('.')[-1])

    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    DirectoryHandler().handle_directory(payload)
