"""Extractor for https://programs.sbs.co.kr/"""

from ..utils.core import (
    Requests, 
    Encode, 
    Logger, 
    Misc, 
    Site,
    DataPayload,
    re,
    json,
    datetime, 
    )

SITE_INFO = Site(hostname="programs.sbs.co.kr", name="SBS Program")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    p_visboards = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/(?:visualboards|multiboards)\/\d+(?:\/?)$')
    p_visboards_s = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/(?:visualboards|multiboards)\/\d+\?[^#]*search_keyword=.*$')
    p_visualboard = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/(?:visualboard|board)\/\d+\?(?=.*\bcmd=[^&#]+)(?=.*\bboard_no=\d+\b).*')
    p_photos = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/photos\/\d+(?:\/?)$')
    p_photos_s = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/photos\/\d+\?[^#]*search=.*$')
    p_photo = re.compile(r'^https:\/\/programs\.sbs\.co\.kr\/[^\/]+\/[^\/]+\/photo\/\d+\/[a-f0-9]+\?(?=.*\balbumid=[a-f0-9]+\b)(?=.*\bphotoid=\d+\b).*')

    root = 'https://programs.sbs.co.kr'
    atic_root = 'https://static.apis.sbs.co.kr'
    a_root = 'https://api.board.sbs.co.kr'

    def get_board_menu(vis_board_no, parent_name):
        site_req = Requests()
        menu_api = "{}/program-api/1.0/menu/{}".format(atic_root, parent_name)
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
        menu_api = "{}/program-api/1.0/multiboards/{}/{}?platform=pc".format(atic_root, parent_name, vis_board_no)
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
        menu_api = "{}/program-api/1.0/menu/{}".format(atic_root, parent_name)
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
    
    def get_individual_info(hd):
        """Get board post"""
        site_req = Requests()
        board_no = hd.split('board_no=')[-1].split('&')[0]
        parent_name = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){1}/([^/?]+)', hd).group(3)
        
        # Get all board information
        menu_api = "{}/program-api/1.0/menu/{}".format(atic_root, parent_name)
        menu_r = site_req.session.get(menu_api).json()
        site_req.session.close()
        category = menu_r['program']['title']
        return category, menu_r, board_no, parent_name

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

        keyword = re.search(r'(?:search=)([^&#]+)', hd)
        if keyword is not None:
            keyword = keyword.group(1)
            keyword = encode._encode_kr(keyword)
            logger.log_info(f"Search keyword: {keyword}")
        
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
                board_list_api = "{}/photo-api/template/1.0/bundle/{}/{}/pc".format(atic_root, program_id, bundle_id)
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
                boards.add('{}/{}/{}/{}/{}/{}?albumid={}'.format(root, path_name, parent_name, type_name, vis_board_no, code[1], i['_id']))
            if len(data) < 15:
                site_req.session.close()
                break
            continue
        
        logger.log_info(f"Found {len(boards)} post(s)")
        for i in boards:
            yield from get_photo_album(i)

    def get_board_list(hd):
        """Get board list"""
        site_req = Requests()
        encode = Encode()
        path_name, parent_name, type_name, vis_board_no = extract_info(hd)
        if type_name == 'multiboards':
            index = re.search(r'#(\d+)$', hd).group(1)
            code_temp = get_multiboard_menu(index, vis_board_no, parent_name)
            board_list_api = "{}/bbs/V2.0/basic/board/photo/main".format(a_root)
        else:
            code_temp = get_board_menu(vis_board_no, parent_name)
            board_list_api = "{}/bbs/V2.0/basic/board/lists".format(a_root)

        keyword = re.search(r'(?:search_keyword=)([^&#]+)', hd)
        if keyword is not None:
            keyword = keyword.group(1)
            keyword = encode._encode_kr(keyword)
            logger.log_info(f"Search keyword: {keyword}")

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
                '_': Misc().get_time()
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
                    boards.add('{}/{}/{}/{}/{}?cmd=multi_list&board_code={}&board_no={}'.format(root, path_name, parent_name, type_name, vis_board_no, i['BOARD_CODE'], i['BOARD_NO']))
                else:
                    boards.add('{}/{}/{}/{}/{}?cmd=view&board_no={}'.format(root, path_name, parent_name, type_name, vis_board_no, i['NO']))
            if len(data) < 16:
                site_req.session.close()
                break
            continue

        logger.log_info(f"Found {len(boards)} post(s)")
        for i in boards:
            yield from get_visual_board(i)

    def get_photo_album(hd):
        """Get photo album"""
        category, menu_r, board_no, parent_name = get_individual_info(hd)
        site_req = Requests()
        bundle_id = re.search(r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){4}/([^/?]+)', hd).group(3)
        photo_album_id = hd.split('albumid=')[-1].split('&')[0]
        programid = menu_r['program']['programid']

        photo_api = "{}/photo-api/template/1.0/bundle/photo/{}/{}/{}/pc".format(atic_root, programid, bundle_id, photo_album_id)
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
        logger.log_extractor_info(f"Album no: {board_no}", post_title, post_date, img_list)

        dir = [SITE_INFO.name, category, f"{post_date_short} {post_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option=None,
            custom_headers=None
        )

        yield payload

    def get_visual_board(hd):
        """Get visual board"""
        category, menu_r, board_no, parent_name = get_individual_info(hd)
        site_req = Requests()
        vis_board_no = re.search(
            r'(?:(https|http)://)?(programs\.sbs\.co\.kr)(?:/[^/]+){3}/([^/?]+)', hd).group(3)
    
        code_temp = get_board_menu(vis_board_no, parent_name)

        site_req = Requests()
    
        for i in code_temp:
            code = i
            api = "{}/bbs/V2.0/basic/board/detail/{}".format(a_root, board_no)
            params = {
                'callback': f'boardViewCallback_{code}',
                'action_type': 'callback',
                'board_code': code,
                'jwt-token': '',
                '_': Misc().get_time()
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
        
        if 'spv.sbs.co.kr' in data['CONTENT']:
            h = data['CONTENT']
            for i in re.findall(r'https?://[^\s"<>]+', h):
                if 'image_id' in i:
                    img_list.add((i, re.search(r"[?&]image_id=([^&]+)", i).group(1)))
                else:
                    img_list.add(i)

        site_req.session.close()
        logger.log_extractor_info(f"Board no: {board_no}", post_title, post_date, img_list)

        dir = [SITE_INFO.name, category, f"{post_date_short} {post_title}"]

        payload = DataPayload(
            directory_format=dir, 
            media=img_list,
            option=None,
            custom_headers={'Referer': root}
        )

        yield payload

    if p_visualboard.match(hd):
        logger.log_info("SBS Visualboard")
        yield from get_visual_board(hd)

    if p_photo.match(hd):
        logger.log_info("SBS Photo")
        yield from get_photo_album(hd)

    if p_visboards_s.match(hd):
        logger.log_info("SBS Visualboard Search")
        yield from get_board_list(hd)

    if p_visboards.match(hd):
        logger.log_info("SBS Visualboards")
        yield from get_board_list(hd)

    if p_photos_s.match(hd):
        logger.log_info("SBS Photos Search")
        yield from get_photo_list(hd)

    if p_photos.match(hd):
        logger.log_info("SBS Photos")
        yield from get_photo_list(hd)