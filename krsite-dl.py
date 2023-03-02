import argparse
import os
import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='?',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
parser.add_argument("-ai", type=str, help="text file containing image urls")
# parser.add_argument("--board-no", type=int, help="The board number from a site (SBS). For example (https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no=438994) will have a board no of 438994")
parser.add_argument("-d", "--destination", type=str, default=".",help="The destination path for the downloaded file")
args = parser.parse_args()
     
        
def check_site(url):
    url = url.strip()
    
    if 'dispatch.co.kr' in url:
        print("Site name 'Dispatch'")
        from_dispatch(url)
    elif 'enews.imbc.com' in url:
        print("Site name 'iMBC News'")
        from_imbcnews(url)
    elif 'newsjamm.co.kr' in url:
        print("Site name 'News Jamm'")
        from_newsjamm(url)
    elif 'sbs.co.kr' in url:
        print("Site name 'SBS'")
        from_sbs(url)
    elif 'post.naver.com' in url:
        print("Site name 'Naver 포스트'")
        from_naverpost(url)
    else:
        # print("URL invalid / Site not supported. [%s]" % url)
        print("Generic Sites %s *may not work" % url.split('/')[2])
        from_generic(url)
        

def from_dispatch(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []
    post_date = soup.find('div', class_='post-date').string.replace('.', '').strip()[:8]
    post_title = soup.find('div', class_='page-post-title').string.strip()

    for i in soup.findAll('img', class_='post-image'):
        if i.get('data-src') != None:
            temp = i.get('data-src')
            img_list.append(temp)
        else:
            temp = i.get('src')
            img_list.append(temp)
    
    print("Title: %s" % post_title)
    print("Date: %s" % post_date[2:])
    print("Found %s image(s)" % len(img_list))
    
    dir_handler_alt(img_list, post_title, post_date[2:])
    
    
def from_imbcnews(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_title = soup.find('h2').text
    post_date = soup.find('span', class_='date').string.replace('-', '')[:8]
    img_list = []

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    for item in soup.findAll('img'):
        if item.get('src') is not None:
            if 'talkimg.imbc.com' in item.get('src'):
                img_list.append('http:' + item.get('src'))
    
    print("Found %s image(s)" % len(img_list))
    dir_handler(img_list, post_title, post_date)
    

def from_newsjamm(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    post_title = soup.find('h1').text
    post_date = soup.find('span', class_='PostContent_statusItem__AgJEE').string.replace('.', '')
    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))

    print("Found %s image(s)" % len(img_list))

    dir_handler(img_list, post_title, post_date)


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

    dir_handler(img_list, post_title, post_date)
    

def from_naverpost(hd):
    def naverpost_topic(hd):
        opt = Options()
        opt.add_argument('--headless')
        w = wd.Chrome(options=opt)
        w.get(hd)
        
        post_list = set()

        btn = w.find_element(By.CLASS_NAME, '_more')

        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False
                for i in w.find_elements(By.CLASS_NAME, 'spot_post_area'):
                    post_list.add('https://post.naver.com' + i.get_attribute('href'))

        w.quit()

        print("Found %s post(s)" % len(post_list))
        
        for i in post_list:
            naverpost_post(i)


    def naverpost_post(hd):
        opt = Options()
        opt.add_argument('--headless')
        w = wd.Chrome(options=opt)
        w.get(hd)

        post_title = w.find_element(By.CLASS_NAME, 'se_textarea').text.replace('\n', ' ')
        post_date = w.find_element(By.CLASS_NAME, 'se_publishDate').text.replace('.', '')[:8]

        img_list = []

        print("Title: %s" % post_title)
        print("Date: %s" % post_date)

        for i in w.find_elements(By.CLASS_NAME, 'se_mediaImage'):
            img_list.append(str(i.get_attribute('src').split('?')[0]))

        w.quit()

        print("Found %s image(s)" % len(img_list))

        dir_handler(img_list, post_title, post_date)


    if 'my.naver' in hd:
        print("Post Dashboard")
        # naverpost_agency(hd)
    elif 'detail.naver' in hd:
        print("Post Topic")
        naverpost_topic(hd)
    elif 'postView.naver' in hd:
        print("Post")
        naverpost_post(hd)


def from_generic(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))
    
    print("Found %s image(s)" % len(img_list))

    dir_handler(img_list)

  
def dir_handler(img_list, title = None, date = None):
    if title != None and date != None:
        dirs = args.destination + '/' + date + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, dirs)


def dir_handler_alt(img_list, title = None, date = None):
    if title != None and date != None:
        dirs = args.destination + '/' + date
        subdirs = dirs + '/' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            if not os.path.exists(dirs + '/' + title):               
                os.makedirs(subdirs)
        else:
            if not os.path.exists(dirs + '/' + title):
                os.makedirs(subdirs)
    else:
        dirs = args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, subdirs)
    

def download_handler(img_list, dirs, chunk_size = 128):
    print("Downloading image(s) to folder: ", dirs)
    
    for img in img_list:
        response = requests.head(img, timeout=5)
        content_length = int(response.headers.get('Content-Length', 0))

        img_name = img.split('/')[-1]

        print("\n[Image] %s" % img_name)

        print("[Metadata] extracting metadata...")

        if os.path.exists(dirs + '/' + img_name):
            print("[Status] This file already exists. Skipping...")
            continue
        
        url_mod_time = response.headers.get('Last-Modified')

        try:
            current_size = os.path.getsize(dirs + "/" + img_name + '.part')
        except FileNotFoundError:
            current_size = 0
        
        if current_size < content_length:
            headers = {'Range': f'bytes={current_size}-{content_length-1}'}
            response = requests.get(img, headers=headers, stream=True)

            with open(dirs + '/' + img_name + '.part', 'ab') as f:
                start = time.time()
                for chunk in response.iter_content(chunk_size=chunk_size):
                    current_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    progress_handler(current_size, content_length, start)
            
            os.rename(dirs + '/' + img_name + '.part', dirs + '/' + img_name)
            
            print("\n[Status] Image %s downloaded" % img_name)

            # Set file and folders modification time
            if url_mod_time:
                print("[Metadata] Embedding metadata to %s" % img_name)
                mod_time = time.strptime(url_mod_time, '%a, %d %b %Y %H:%M:%S %Z')
                os.utime(dirs + '/' + img_name, (time.time(), time.mktime(mod_time)))
        
        if url_mod_time:
            os.utime(dirs, (time.time(), time.mktime(mod_time)))

                

    
def progress_handler(current_size, content_length, start):
    elapsed_time = time.time() - start
    bandwidth = current_size / elapsed_time
    percent = (current_size / content_length) * 100
    eta = (content_length - current_size) / bandwidth
    
    if bandwidth >= 1024**2:
        bandwidth_str = f"{bandwidth/1024**2:.2f}MB/s"
    else:
        bandwidth_str = f"{bandwidth/1024:.2f}KB/s"

    if content_length >= 1024**2:
        content_length_str = f"{content_length/1024**2:.2f}MB"
        current_size_str = f"{current_size/1024**2:.2f}"
    else:
        content_length_str = f"{content_length/1024:.2f}KB"
        current_size_str = f"{current_size/1024:.2f}"
    
    if percent == 100:
        percent_str = f"\033[32m{percent:.2f}%\033[37m"
    else:
        percent_str = f"{percent:.2f}%"
    if eta == 0:
        eta_str = f"                 "
    else:
        if eta >= 60:
            eta = eta / 60
            if eta >= 60:
                eta = eta / 60
                if eta >= 24:
                    eta = eta / 24
                    eta_str = f"\033[32m, ETA:{int(eta)} day(s)\033[0m"
                else:
                    eta_str = f"\033[32m, ETA:{int(eta)} h\033[0m"
            else:
                eta_str = f"\033[32m, ETA:{int(eta)} m\033[0m"
        else:
            eta_str = f"\033[32m, ETA:{int(eta)} s\033[0m"

    print(f"\r[Progress] {current_size_str}/{content_length_str} ({percent_str}) \033[36m@\033[37m {bandwidth_str}{eta_str}", end="")


def main():
    if args.a:
        with open(args.a, 'r') as f:
            for line in f:
                if line[0] == '#' or line[0] == ';' or line[0] == ']':
                    continue
                elif line != '\n':
                    check_site(line)
    else:
        check_site(args.url)

if __name__ == '__main__':
    main()