"""Extractor for https://k-odyssey.com"""

import datetime
import re

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="k-odyssey.com", name="K-odyssey")


def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)

    img_list = []

    post_title = soup.find('div', class_='viewTitle').find('h1').text.strip()
    post_date = soup.find('div', class_='dd').text.strip()
    post_date_short = re.sub('[\u3131-\uD7A3]+|\/|-|\s', '', post_date)[2:8]
    content = soup.find('div', class_='sliderkit-panels')

    for i in content.find_all('img'):
        img_list.append('https://k-odyssey.com' +
                        i['src'].replace('_thum', ''))

    post_date = re.sub('[\u3131-\uD7A3]+|\/|-|\s+', '', post_date)
    post_date = post_date[:8] + ' ' + post_date[8:]
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %H:%M:%S')

    site_req.session.close()
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, post_date_short, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    DirectoryHandler().handle_directory(payload)
