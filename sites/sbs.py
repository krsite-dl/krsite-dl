import requests
import json
import down.directory as dir

def from_sbs(hd):
    board_id = hd.split('=')[-1]
    print("Board no: %s" % board_id)

    code = ''

    if '69423' in hd:
        code = 'runningman_photo'
    elif '65942' in hd and 'pdnote_hotissue' in hd:
        code = 'pdnote_hotissue'
    elif '54795' in hd or '65942' in hd:
        code = 'inkigayo_pt01'
    elif '68458' in hd:
        code = 'inkigayo_pt02'
    elif '71656' in hd:
        code = 'inkigayo_pt05'
    elif '76371' in hd:
        code = '2022sbsgayo_pt'
    elif '58358' in hd:
        code = 'theshow04_pt'
    # add more to your liking. (elif 'board_id' in hd: code = 'board_code')

    ###########TOKEN############
    token = '1676983404524'
    ############################

    api = 'https://api.board.sbs.co.kr/bbs/V2.0/basic/board/detail/'
    params = '%s?callback=boardViewCallback_%s&action_type=callback&board_code=%s&jwt-token=&_=%s' % (board_id, code, code, token)

    r = requests.get(api + params)
    json_data = r.text
    json_data = json_data.split('boardViewCallback_%s(' % code)[1]
    json_data = json_data.replace(');', '')
    json_data = json.loads(json_data)
    
    data = json_data['Response_Data_For_Detail']
    post_title = data['TITLE'].strip()
    post_date = data['REG_DATE'].replace('-', '')[:8].strip()
    img_list = []

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    for i in data['URL']:
        if 'http' not in i:
            img_list.append('http:' + str(i))
        else:
            img_list.append(str(i))
    
    
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list, post_title, post_date)