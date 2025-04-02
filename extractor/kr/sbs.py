"""Extractor for https://programs.sbs.co.kr/"""

import datetime
import time
import json
import re

from common.common_modules import Requests, Encode
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="programs.sbs.co.kr", name="SBS Program")


def get_data(hd):
    """Get data"""

    def get_time():
        ########### TOKEN############
        current_milli_time = int(round(time.time() * 1000))
        return str(current_milli_time)
        ############################

    def get_board_menu(vis_board_no, parent_name):
        site_req = Requests()
        menu_api = "https://static.apis.sbs.co.kr/program-api/1.0/menu/{}".format(parent_name)
        menu_r = site_req.session.get(menu_api).json()
        site_req.session.close()
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
        return code_temp
    
    def get_multiboard_menu(index, vis_board_no, parent_name):
        site_req = Requests()
        menu_api = "https://static.apis.sbs.co.kr/program-api/1.0/multiboards/{}/{}?platform=pc".format(parent_name, vis_board_no)
        menu_r = site_req.session.get(menu_api).json()
        site_req.session.close()
        all_board = []

        for idx, menu in enumerate(menu_r['category']):
            board_code = menu['board_code'].split(',')
            all_board.append({str(idx): board_code})
        
        code_temp = []
        for i in all_board:
            for key, value in i.items():
                if key == index:
                    for j in value:
                        code_temp.append(j.strip())
        return code_temp
    
    def get_photo_menu(vis_board_no, parent_name):
        site_req = Requests()
        menu_api = "https://static.apis.sbs.co.kr/program-api/1.0/menu/{}".format(parent_name)
        menu_r = site_req.session.get(menu_api).json()
        site_req.session.close()
        all_board = []
        def iterate_menu(menu):
            if 'photo' in menu:
                program_id = menu['programid']
                menu_id = menu['mnuid']
                bundle_id = menu['photo']['bundle_id']
                all_board.append({menu_id: [program_id, bundle_id]})
                
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
                    code_temp.append(value)
        return code_temp

    def extract_info(url):
        path_name = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){0}/([^/?]+)', url).group(3)
        parent_name = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){1}/([^/?]+)', url).group(3)
        type_name = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){2}/([^/?]+)', url).group(3)
        vis_board_no = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){3}/([^/?]+)', url).group(3)
        return path_name, parent_name, type_name, vis_board_no

    def get_photo_list(hd):
        """Get photo list"""
        site_req = Requests()
        encode = Encode()
        path_name, parent_name, type_name, vis_board_no = extract_info(hd)
        code_temp = get_photo_menu(vis_board_no, parent_name)
        board_list_api = f"https://static.apis.sbs.co.kr/photo-api/template/1.0/bundle/"

        keyword = re.search(r'(?:search=)([^&#]+)', hd)
        if keyword is not None:
            keyword = keyword.group(1)
            keyword = encode._encode_kr(keyword)
            print(f"Search keyword: {keyword}")
        
        boards = set()
        code = ''
        data = []

        params = {
                'offset': 0,
                'limit': 15,
                'sort': 'new'
            }
        if keyword is not None:
            params['searchkeyword'] = keyword
        while True:
            for i in code_temp:
                code = i
                program_id, bundle_id = code
                board_list_api = "https://static.apis.sbs.co.kr/photo-api/template/1.0/bundle/{}/{}/pc".format(program_id, bundle_id)
                r = site_req.session.get(board_list_api, params=params)
                if 'Server Error' not in r.text:
                    site_req.session.close()
                    break
            r = site_req.session.get(board_list_api, params=params)
            json_data = r.text
            json_data = json.loads(json_data)
            data = json_data['list']
            params['offset'] += 15
            for i in data:
                boards.add('https://programs.sbs.co.kr/{}/{}/{}/{}/{}?albumid={}'.format(path_name, parent_name, type_name, vis_board_no, code[1], i['_id']))
            if len(data) < 15:
                site_req.session.close()
                break
            continue
        
        print(f"Found {len(boards)} post(s)")
        for i in boards:
            get_board_post(i)

    def get_board_list(hd):
        """Get board list"""
        site_req = Requests()
        encode = Encode()
        path_name, parent_name, type_name, vis_board_no = extract_info(hd)
        if type_name == 'multiboards':
            index = re.search(r'#(\d+)$', hd).group(1)
            code_temp = get_multiboard_menu(index, vis_board_no, parent_name)
            board_list_api = f"https://api.board.sbs.co.kr/bbs/V2.0/basic/board/photo/main"
        else:
            code_temp = get_board_menu(vis_board_no, parent_name)
            board_list_api = f"https://api.board.sbs.co.kr/bbs/V2.0/basic/board/lists"

        keyword = re.search(r'(?:search_keyword=)([^&#]+)', hd)
        if keyword is not None:
            keyword = keyword.group(1)
            keyword = encode._encode_kr(keyword)
            print(f"Search keyword: {keyword}")

        boards = set()
        code = ''
        data = []

        params = {
                'callback': '',
                'offset': 0,
                'limit': 16,
                'action_type': 'callback',
                'board_code': '',
                'searchOption': 'title',
                'jwt-token': '',
                '_': get_time()
            }
        if type_name == 'multiboards':
            params['menuid'] = vis_board_no
        if keyword is not None:
            params['searchKeyword'] = keyword
        while True:
            for i in code_temp:
                code = i
                params['callback'] = f'boardListCallback_{code}'
                params['board_code'] = code
                r = site_req.session.get(board_list_api, params=params)
                if 'err_code' not in r.text:
                    site_req.session.close()
                    break
            
            r = site_req.session.get(board_list_api, params=params)
            json_data = r.text
            json_data = json_data.split('boardListCallback_%s(' % code)[1]
            json_data = json_data.rstrip(');')
            json_data = json.loads(json_data)
            
            if 'list' not in json_data:
                json_data = {'list': json_data}
            data = json_data['list']
            params['offset'] += 15
            
            for i in data:
                if type_name == 'multiboards':
                    boards.add('https://programs.sbs.co.kr/{}/{}/{}/{}?cmd=multi_list&board_code={}&board_no={}'.format(path_name, parent_name, type_name, vis_board_no, i['BOARD_CODE'], i['BOARD_NO']))
                else:
                    boards.add('https://programs.sbs.co.kr/{}/{}/{}/{}?cmd=view&board_no={}'.format(path_name, parent_name, type_name, vis_board_no, i['NO']))
            if len(data) < 16:
                site_req.session.close()
                break
            continue

        print(f"Found {len(boards)} post(s)")
        for i in boards:
            get_board_post(i)

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
        
            code_temp = get_board_menu(vis_board_no, parent_name)

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
                    '_': get_time()
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



    if 'search_keyword=' in hd:
        get_board_list(hd)
    elif 'search=' in hd and 'photo' in hd:
        get_photo_list(hd)
    else:
        get_board_post(hd)