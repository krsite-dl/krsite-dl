"""Extractor for https://enews.imbc.com"""

import datetime, re

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="enews.imbc.com", name="iMBC News")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('h2').text.strip()
    post_date = soup.find('span', class_='date').text.strip()
    post_date_short = post_date.replace('-', '')
    post_date_short = re.sub('[\u3131-\uD7A3]+', '', post_date_short)[2:8]

    img_list = []

    for item in soup.findAll('img'):
        if item.get('src') is not None:
            if 'talkimg.imbc.com' in item.get('src'):
                img_list.append('http:' + item.get('src'))

    print("Found %s image(s)" % len(img_list))

    post_date = re.sub('[\u3131-\uD7A3]+', '', post_date)
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')

    site_req.session.close()
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, post_date_short, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    DirectoryHandler().handle_directory(payload)
