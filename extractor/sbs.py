import time
import datetime
import requests
import json
import down.directory as dir

def from_sbs(hd):
    print("Url: %s" % hd)
    board_no = hd.split('board_no=')[-1].split('&')[0]
    print("Board no: %s" % board_no)

    code = ''

    # ADD MORE KEY AND VALUE HERE
    """
    https://programs.sbs.co.kr/enter/gayo/visualboard/board_id?
    board_code can be found in the api. look at response in the network tab.
    FORMAT: 'board_id': 'board_code
    """
    code_dict = {
        '69423': ['runningman_photo'],
        '65942': ['pdnote_hotissue', 'inkigayo_pt01'],
        '54795': ['inkigayo_pt01'],
        '68458': ['inkigayo_pt02'],
        '71199': ['inkigayo_pt03'],
        '71279': ['inkigayo_pt04'],
        '71656': ['inkigayo_pt05'],
        '76748': ['inkigayo_pt06'],
        '76371': ['2022sbsgayo_pt'],
        '58358': ['theshow04_pt']
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
        print(i)
        code = i
        api = 'https://api.board.sbs.co.kr/bbs/V2.0/basic/board/detail/'
        params = '%s?callback=boardViewCallback_%s&action_type=callback&board_code=%s&jwt-token=&_=%s' % (board_no, code, code, token)

        print(api + params)
        r = requests.get(api + params)
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

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    for i in data['URL']:
        if 'http' not in i:
            img_list.append('http:' + str(i))
        else:
            img_list.append(str(i))
    
    
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list, post_title, post_date_short, post_date)