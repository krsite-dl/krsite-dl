"""Extractor for https://harpersbazaar.co.kr"""

import datetime

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="harpersbazaar.co.kr", name="Harper's Bazaar Korea")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')[
        'content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S')

    content = soup.find('div', class_='atc_content')

    img_list = []
    for item in content.findAll('img'):
        if item.get('lazy') is not None or item.get('src') is not None:
            img_list.append(item.get('lazy') or item.get('src'))

    head_img = soup.find('div', class_='article_head')

    if head_img.get('style') is not None:
        img_list.append(head_img['style'].split(
            'url(')[1].split(')')[0].replace('"', ''))

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
