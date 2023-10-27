import requests
import datetime
import time
import json

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from rich import print

SITE_INFO = Site(hostname="programs.sbs.co.kr", name="SBS Program", location="KR")

def get_data(hd):
    board_no = hd.split('board_no=')[-1].split('&')[0]
    print(f"Board no: {board_no}")

    code = ''

    # ADD MORE KEY AND VALUE HERE
    code_dict = {
        '69423': ['runningman_photo'],
        '65942': ['pdnote_hotissue', 'inkigayo_pt01'],
        '54795': ['inkigayo_pt01'],
        '68458': ['inkigayo_pt02'],
        '71199': ['inkigayo_pt03'],
        '71279': ['inkigayo_pt04'],
        '71656': ['inkigayo_pt05'],
        '76748': ['inkigayo_pt06'],
        '70688': ['2021sbsgayo_pt1'],
        '70687': ['2021sbsgayo_pt2'],
        '76371': ['2022sbsgayo_pt'],
        '58358': ['theshow04_pt'],
        '65175': ['sbspr_02'],
        '4295': ['sbssuperconcert_pt']
    }

    code_temp = []

    for key, value in code_dict.items():
        if key in hd:
            code_temp.extend(value)

    ###########TOKEN############
    current_milli_time = int(round(time.time() * 1000))
    token = str(current_milli_time)
    ############################

    for i in code_temp:
        print(f"[green]Code:[/green] {i}")
        code = i
        api = f"https://api.board.sbs.co.kr/bbs/V2.0/basic/board/detail/{board_no}"

        params = {
            'callback': f'boardViewCallback_{code}',
            'action_type': 'callback',
            'board_code': code,
            'jwt-token': '',
            '_': token
        }

        r = requests.get(api, params, headers={'User-Agent': InitUserAgent().get_user_agent()})
        if 'err_code' not in r.text:
            break

    json_data = r.text
    json_data = json_data.split('boardViewCallback_%s(' % code)[1]
    json_data = json_data.replace(');', '')
    json_data = json.loads(json_data)
    
    data = json_data['Response_Data_For_Detail']
    post_title = data['TITLE'].strip()
    post_date = data['REG_DATE'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    img_list = []

    print(f"Title: {post_title}")
    print(f"Date: {post_date}")

    for i in data['URL']:
        if 'http' not in i:
            img_list.append('http:' + str(i))
        else:
            img_list.append(str(i))
    
    
    print(f"Found {len(img_list)} image(s)")

    payload = ScrapperPayload(
        title=post_title,
        shortDate=post_date_short,
        mediaDate=post_date,
        site=SITE_INFO.name,
        series=None,
        writer=None,
        location=SITE_INFO.location,
        media=img_list,
    )
    
    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)