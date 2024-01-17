"""Extractor for https://dispatch.co.kr"""

import datetime

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="dispatch.co.kr", name="Dispatch", location="KR")


def get_data(hd):
    site_parser = SiteParser()
    site_requests = Requests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    img_list = []
    post_date = soup.find('div', class_='post-date').text.strip()
    post_title = soup.find('div', class_='page-post-title').string.strip()
    post_date_short = post_date.replace('.', '')[2:8]

    for i in soup.findAll('img', class_='post-image'):
        if i.get('data-src') is not None:
            if i.get('data-src').startswith('<' or '>'):
                continue
            temp = i.get('data-src')
            img_list.append(temp)
        else:
            if i.get('src').startswith('<' or '>'):
                continue
            temp = i.get('src')
            img_list.append(temp)

    post_date = post_date[:19].replace('.', '')
    if '오전' in post_date:
        post_date = datetime.datetime.strptime(
            post_date.replace('오전', 'AM'), '%Y%m%d %p %I:%M')
    elif '오후' in post_date:
        post_date = datetime.datetime.strptime(
            post_date.replace('오후', 'PM'), '%Y%m%d %p %I:%M')

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
