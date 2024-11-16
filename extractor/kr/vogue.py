"""Extractor for https://vogue.co.kr"""

import datetime
import re

from pytz import timezone
from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="vogue.co.kr", name="Vogue Korea")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='contt')
    content2 = soup.find('div', class_='masonry_grid')

    img_list = []

    for item in content.findAll('img'):
        if item.get('data-src') is not None:
            i = item.get('data-src')
            img_list.append(i.split('-')[0] + '.' + i.split('.')[-1])

    for item in content2.findAll('img'):
        if item.get('data-src') is not None:
            i = item.get('data-src')
            img_list.append(i.split('-')[0] + '.' + i.split('.')[-1])

    pattern0 = re.compile(r'style="background-image: url\(([^)]+)\)')
    matches = pattern0.findall(soup.text)
    for match in matches:
        src = match.split('-')[0] + '.' + i.split('.')[-1]
        img_list.append(src)

    site_req.session.close()
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    DirectoryHandler().handle_directory(payload)
