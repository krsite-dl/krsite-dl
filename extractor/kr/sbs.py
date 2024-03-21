"""Extractor for https://programs.sbs.co.kr/"""

import datetime
import time
import json
import re

from rich import print
from common.common_modules import Requests
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="programs.sbs.co.kr", name="SBS Program")


def get_data(hd):
    """Get data"""
    site_req = Requests()
    board_no = hd.split('board_no=')[-1].split('&')[0]
    parent_name = re.search(
        r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){1}/([^/?]+)', hd).group(3)
    vis_board_no = re.search(
        r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){3}/([^/?]+)', hd).group(3)
    print(f"Board no: {board_no}")


    # Get all board information
    menu_api = "https://static.apis.sbs.co.kr/program-api/1.0/menu/"
    menu_r = site_req.session.get(menu_api + parent_name).json()
    category = menu_r['program']['title']
    all_board = []

    def iterate_menu(menu):
        if menu['board_code'] is not None:
            menu_id = menu['mnuid']
            board_code = menu['board_code'].split(',')
            all_board.append({menu_id: board_code})

    for menu in menu_r['menus']:
        iterate_menu(menu)
        # Check if there are submenus
        if menu['submenus']:
            for submenu in menu['submenus']:
                iterate_menu(submenu)

    code_temp = []

    for i in all_board:
        for key, value in i.items():
            if key == vis_board_no:
                for j in value:
                    code_temp.append(j.strip())

    ########### TOKEN############
    current_milli_time = int(round(time.time() * 1000))
    token = str(current_milli_time)
    ############################

    code = ''

    print(code_temp)
    
    for i in code_temp:
        code = i
        api = f"https://api.board.sbs.co.kr/bbs/V2.0/basic/board/detail/{board_no}"

        params = {
            'callback': f'boardViewCallback_{code}',
            'action_type': 'callback',
            'board_code': code,
            'jwt-token': '',
            '_': token
        }

        r = site_req.session.get(api, params=params)

        if 'err_code' not in r.text:
            break

    json_data = r.text
    json_data = json_data.split('boardViewCallback_%s(' % code)[1]
    json_data = json_data.rstrip(');')
    json_data = json.loads(json_data)

    data = json_data['Response_Data_For_Detail']
    post_title = data['TITLE'].strip()
    post_date = data['REG_DATE'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    img_list = set()

    for i in data['URL']:
        if 'http' not in i:
            img_list.add('http:' + str(i))
        else:
            img_list.add(str(i))

    site_req.session.close()
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, category, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    DirectoryHandler().handle_directory(payload)
