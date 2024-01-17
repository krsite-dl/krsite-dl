"""Extractor for https://wkorea.com"""

import datetime
import re

from pytz import timezone
from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="wkorea.com", name="W Korea")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_requests = Requests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    contents = soup.find('div', class_='masonry_grid')

    if contents is None:
        contents = soup.find('div', class_='post_content')

    img_list = set()
    for item in contents.findAll('img'):
        i = item.get('src')
        if i.startswith('http'):
            img_list.add(re.sub(r'-\d+x\d+', '', i))

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
