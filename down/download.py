import requests
import os
import time
import pytz
from rich.progress import Progress
from urllib.parse import unquote

def download_handler(img_list, dirs, post_date, loc, chunk_size = 128):
    print("Downloading image(s) to folder: ", dirs)
    for img in img_list:
        try:
            response = requests.head(img, timeout=60)
        except requests.exceptions.Timeout:
            print("Request timeout. Skipping...")
        
        content_length = int(response.headers.get('Content-Length', 0))
        
        img_name = img.split('/')[-1]

        decoded = unquote(img_name).strip()

        if '%EC' in decoded or '%EB' in decoded:
            korean_filename = decoded.encode('utf-8')
        else:
            try:
                korean_filename = decoded.encode('euc-kr')
            except UnicodeDecodeError:
                korean_filename = decoded.encode('euc-kr', errors='ignore')
        
        img_name = korean_filename

        img_name = img_name.decode('euc-kr')

        print("[Source URL] %s" % img)
        print("[Image Name] %s" % img_name)


        if os.path.exists(dirs + '/' + img_name):
            print("[Status] This file already exists. Skipping...")
            continue

        try:
            current_size = os.path.getsize(dirs + "/" + img_name + '.part')
        except FileNotFoundError:
            current_size = 0
        
        if current_size < content_length:
            headers = {'Range': f'bytes={current_size}-{content_length-1}'}
            response = requests.get(img, headers=headers, stream=True)

            with open(dirs + '/' + img_name + '.part', 'ab') as f:
                with Progress() as progress:
                    task = progress.add_task("[cyan]Downloading...", total=content_length)
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        current_size += len(chunk)
                        f.write(chunk)
                        f.flush()
                        progress.update(task, completed=current_size)
            
            os.rename(dirs + '/' + img_name + '.part', dirs + '/' + img_name)
            
            print("\n[Status] Image %s downloaded" % img_name)

            # Set file and folders modification time
            if loc == "KR":
                utc = pytz.timezone("Asia/Seoul")
            elif loc == "JP":
                utc = pytz.timezone("Asia/Tokyo")
            elif loc == "SG":
                utc = pytz.timezone("Asia/Singapore")
            
            dt = post_date
            dt = utc.localize(dt)
            timestamp = int(dt.timestamp())
            
            # print(timestamp)
            # print(dt)

            os.utime(dirs + '/' + img_name, (timestamp, timestamp))
        os.utime(dirs, (timestamp, timestamp))


def download_handler_naver(img_list, dirs, post_date, chunk_size = 128):
    print("Downloading image(s) to folder: ", dirs)
    for img in img_list:
        try:
            response = requests.head(img, timeout=60)
        except requests.exceptions.Timeout:
            print("Request timeout. Skipping...")
        
        content_length = int(response.headers.get('Content-Length', 0))
        
        img_name = img.split('/')[-1]

        decoded = unquote(img_name).strip()

        if '%EC' in decoded or '%EB' in decoded:
            korean_filename = decoded.encode('utf-8')
        else:
            try:
                korean_filename = decoded.encode('euc-kr')
            except UnicodeDecodeError:
                korean_filename = decoded.encode('euc-kr', errors='ignore')
        
        img_name = korean_filename

        img_name = img_name.decode('euc-kr')

        print("[Source URL] %s" % img)
        print("[Image Name] %s" % img_name)


        if os.path.exists(dirs + '/' + img_name):
            print("[Status] This file already exists. Skipping...")
            continue
        

        try:
            current_size = os.path.getsize(dirs + "/" + img_name + '.part')
        except FileNotFoundError:
            current_size = 0
        
        if current_size < content_length:
            headers = {'Range': f'bytes={current_size}-{content_length-1}'}
            response = requests.get(img, headers=headers, stream=True)

            with open(dirs + '/' + img_name + '.part', 'ab') as f:
                with Progress() as progress:
                    task = progress.add_task("[cyan]Downloading...", total=content_length)
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        current_size += len(chunk)
                        f.write(chunk)
                        f.flush()
                        progress.update(task, completed=current_size)
            
            os.rename(dirs + '/' + img_name + '.part', dirs + '/' + img_name)


            # Set file and folders modification time
            utc = pytz.timezone("Asia/Seoul")
            dt = post_date
            dt = utc.localize(dt)
            
            timestamp = int(dt.timestamp())
            # print(timestamp)
            # print(dt)

            os.utime(dirs + '/' + img_name, (timestamp, timestamp))
        os.utime(dirs, (timestamp, timestamp))


def download_handler_news1(img_list, dirs, post_date, post_date_short, title, loc, chunk_size = 128):
    print("Downloading image(s) to folder: ", dirs)
    for img in img_list:
        try:
            response = requests.head(img, timeout=60)
        except requests.exceptions.Timeout:
            print("Request timeout. Skipping...")
        
        content_length = int(response.headers.get('Content-Length', 0))
        
        img_ext = img.split('.')[-1]

        img_name = f'{post_date_short} {title}.{img_ext}'

        print("[Source URL] %s" % img)
        print("[Image Name] %s" % img_name)


        if os.path.exists(dirs + '/' + img_name):
            print("[Status] This file already exists. Skipping...")
            continue

        try:
            current_size = os.path.getsize(dirs + "/" + img_name + '.part')
        except FileNotFoundError:
            current_size = 0
        
        if current_size < content_length:
            headers = {'Range': f'bytes={current_size}-{content_length-1}'}
            response = requests.get(img, headers=headers, stream=True)

            with open(dirs + '/' + img_name + '.part', 'ab') as f:
                with Progress() as progress:
                    task = progress.add_task("[cyan]Downloading...", total=content_length)
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        current_size += len(chunk)
                        f.write(chunk)
                        f.flush()
                        progress.update(task, completed=current_size)
            
            os.rename(dirs + '/' + img_name + '.part', dirs + '/' + img_name)
            

            # Set file and folders modification time
            if loc == "KR":
                utc = pytz.timezone("Asia/Seoul")
            elif loc == "JP":
                utc = pytz.timezone("Asia/Tokyo")
            elif loc == "SG":
                utc = pytz.timezone("Asia/Singapore")
            
            dt = post_date
            dt = utc.localize(dt)
            timestamp = int(dt.timestamp())
            
            # print(timestamp)
            # print(dt)
            print(timestamp)

            os.utime(dirs + '/' + img_name, (timestamp, timestamp))
        os.utime(dirs, (timestamp, timestamp))


def download_handler_alt(img, dirs, chunk_size = 128):
    print("Downloading image(s) to folder: ", dirs)
    try:
        response = requests.head(img, timeout=60)
    except requests.exceptions.Timeout:
        print("Request timeout. Skipping...")
    content_length = int(response.headers.get('Content-Length', 0))
    print(content_length)
    img_name = img.split('/')[-1]

    decoded = unquote(img_name).strip()

    if '%EC' in decoded or '%EB' in decoded:
        korean_filename = decoded.encode('utf-8')
    else:
        try:
            korean_filename = decoded.encode('euc-kr')
        except UnicodeDecodeError:
            korean_filename = decoded.encode('euc-kr', errors='ignore')
    
    img_name = korean_filename

    img_name = img_name.decode('euc-kr')

    print("\n[Image Name] %s" % img_name)


    if os.path.exists(dirs + '/' + img_name):
        print("[Status] This file already exists. Skipping...")
        return
    
    url_mod_time = response.headers.get('Last-Modified')

    try:
        current_size = os.path.getsize(dirs + "/" + img_name + '.part')
    except FileNotFoundError:
        current_size = 0
    
    if current_size < content_length:
        headers = {'Range': f'bytes={current_size}-{content_length-1}'}
        response = requests.get(img, headers=headers, stream=True)

        with open(dirs + '/' + img_name + '.part', 'ab') as f:
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading...", total=content_length)
                for chunk in response.iter_content(chunk_size=chunk_size):
                    current_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    progress.update(task, completed=current_size)
        
        os.rename(dirs + '/' + img_name + '.part', dirs + '/' + img_name)
        

        # Set file and folders modification time
        if url_mod_time:
            print("[Metadata] Embedding metadata to %s" % img_name)
            mod_time = time.strptime(url_mod_time, '%a, %d %b %Y %H:%M:%S %Z')
            os.utime(dirs + '/' + img_name, (time.time(), time.mktime(mod_time)))
    
    if url_mod_time:
        os.utime(dirs, (time.time(), time.mktime(mod_time)))