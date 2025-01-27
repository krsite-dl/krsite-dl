"""Extractor for https://programs.sbs.co.kr/"""

import datetime
import time
import json
import re

from rich import print
from common.common_modules import Requests, Encode
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="programs.sbs.co.kr", name="SBS Program")


def get_data(hd):
    """Get data"""

    # def get_board_list(hd):
    #     """Get board list"""
    #     '''
    #         https://programs.sbs.co.kr/enter/gayo/visualboards/54795?cmd=list&search_option=title&search_keyword=%EB%89%B4%EC%A7%84%EC%8A%A4
    #         https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no=462498

    #         https://api.board.sbs.co.kr/bbs/V2.0/basic/board/lists?callback=boardListCallback_inkigayo_pt01&offset=0&limit=16&action_type=callback&board_code=inkigayo_pt01&searchOption=title&searchKeyword=뉴진스&jwt-token=&_=1732246574524
    #     '''


    #     code_temp, token, board_no, category, programid = menu_api(hd)
    #     site_req = Requests()
    #     encode = Encode()

    #     keyword = hd.split('search_keyword=')[1].split('&')[0]
    #     keyword = encode._encode_kr(keyword)

    #     board_list_api = f"https://api.board.sbs.co.kr/bbs/V2.0/basic/board/lists"

    #     boards = []
    #     code = ''
    #     for i in code_temp:
    #         code = i

    #         params = {
    #             'callback': f'boardListCallback_{code}',
    #             'offset': 0,
    #             'limit': 16,
    #             'action_type': 'callback',
    #             'board_code': code,
    #             'searchOption': 'title',
    #             'searchKeyword': keyword,
    #             'jwt-token': '',
    #             '_': token
    #         }


    #         r = site_req.session.get(board_list_api, params=params)

    #         if 'err_code' not in r.text:
    #             break


    #     json_data = r.text
    #     json_data = json_data.split('boardListCallback_%s(' % code)[1]
    #     json_data = json_data.rstrip(');')
    #     json_data = json.loads(json_data)

    #     data = json_data['list']

    #     for i in data:
    #         boards.append(i['NO'])


    def get_board_post(hd):
        """Get board post"""

        site_req = Requests()
        board_no = hd.split('board_no=')[-1].split('&')[0]
        parent_name = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){1}/([^/?]+)', hd).group(3)
        
        # Get all board information
        menu_api = "https://static.apis.sbs.co.kr/program-api/1.0/menu/"
        menu_r = site_req.session.get(menu_api + parent_name).json()
        site_req.session.close()
        category = menu_r['program']['title']

        def photo_album():
            """Get photo album"""
            bundle_id = re.search(r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){4}/([^/?]+)', hd).group(3)
            photo_album_id = hd.split('albumid=')[-1].split('&')[0]
            programid = menu_r['program']['programid']


            photo_api = "https://static.apis.sbs.co.kr/photo-api/template/1.0/bundle/photo/{}/{}/{}/pc".format(programid, bundle_id, photo_album_id)

            r = site_req.session.get(photo_api)
            json_data = r.json()

            data = json_data['photo']
            post_title = data['title']
            post_date = data['reg_date'].strip()
            post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d')
            post_date_short = post_date.strftime('%y%m%d')
            
            img_list = set()

            img_list.add(re.sub(r'https?://|://|//', 'https://', data['image_url']))

            for i in json_data['list']:
                img_list.add(i['full_size_image_url'])
            
            site_req.session.close()
            print(f"Title: {post_title}")
            print(f"Date: {post_date}")
            print(f"Found {len(img_list)} image(s)")

            dir = [SITE_INFO.name, category, f"{post_date_short} {post_title}"]

            payload = DataPayload(
                directory_format=dir,
                media=img_list,
                option=None,
                custom_headers=None
            )

            DirectoryHandler().handle_directory(payload)

        def visual_board():
            """Get visual board"""
            vis_board_no = re.search(
                r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){3}/([^/?]+)', hd).group(3)
        
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

            print(f"Board no: {board_no}")

            site_req = Requests()

        
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
                custom_headers={'Referer': 'https://programs.sbs.co.kr'}
            )

            DirectoryHandler().handle_directory(payload)


        if 'photo' in hd:
            photo_album()
        else:
            visual_board()



    if 'search_keyword' in hd:
        pass
    else:
        get_board_post(hd)