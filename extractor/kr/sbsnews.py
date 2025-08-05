"""Extractor for https://ent.sbs.co.kr"""

import datetime, re

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="ent.sbs.co.kr", name="SBS News")


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
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, post_date_short, {post_title}]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    DirectoryHandler().handle_directory(payload)
