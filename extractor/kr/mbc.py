"""Extractor for https://mbc.co.kr/"""

import datetime
import re

from common.common_modules import Requests
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="mbc.co.kr", name="MBC")


def get_data(hd):
    """Get data"""
    # https://with.mbc.co.kr/m/pr/press/view.html?idx=32262
    # https://with.mbc.co.kr/pr/press/view.html?idx=32262

    BASE = r"(?:https?://)?(with\.mbc\.co\.kr)?(\.m)?"
    pattern = BASE + r"(/pr.press/view.html)"
    pattern2 = BASE + r"(/photo/view.html)"

    idx = hd.split('idx=')[-1].split('&')[0]
    img_api = f'https://mbcinfo.imbc.com/api/download?file='

    
    def mbc_photo(idx):
        api = f'https://mbcinfo.imbc.com/api/photo/m_info?intIdx={idx}'

        site_req = Requests()
        r = site_req.session.get(api)
        json_data = r.json()

        post_title = json_data['list'][0]['title']
        post_date = json_data['list'][0]['reg_dt']
        post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
        post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        for i in json_data['list']:
            img_list.append(f"{img_api}{i['photo_fullpath']}")

        site_req.session.close()
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

    
    def mbc_press(idx):
        api = f'https://mbcinfo.imbc.com/api/press/info?intIdx={idx}'

        site_req = Requests()
        r = site_req.session.get(api)
        json_data = r.json()

        post_title = json_data['info']['info']['title']
        post_date = json_data['info']['info']['reg_dt']
        post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
        post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        for i in json_data['file']:
            img_list.append(f"{img_api}{i['file_fullpath']}")

        site_req.session.close()
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

    if re.search(pattern2, hd):
        mbc_photo(idx)
    elif re.search(pattern, hd):
        mbc_press(idx)