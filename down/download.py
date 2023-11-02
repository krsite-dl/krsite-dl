import requests
import os
import re
import time
import pytz
import subprocess

from rich.progress import Progress
from urllib.parse import unquote, urlparse
from client.user_agent import InitUserAgent
import krsite_dl as kr

class DownloadHandler():
    def __init__(self):
        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]'

    
    # sanitize string to remove windows reserved characters
    def __sanitize_string(self, string):
        if not self.args.no_windows_filenames:
            string = re.sub(self.reserved_pattern, '', string)
        return string
    

    # location list for timezone
    def _location(self, loc):
        # list country codes here as json so i can call them by matching its keys
        country_codes = {
            "KR": "Asia/Seoul", "JP": "Asia/Tokyo", "SG": "Asia/Singapore"
        }

        return country_codes.get(loc, "UTC")
        

    # korean filename encoder
    def _encode_kr(self, img_name):
        # img = img_name.split('/')[-1]
        decoded = unquote(img_name).strip()

        if '%EC' in decoded or '%EB' in decoded:
            korean_filename = decoded.encode('utf-8')
        else:
            korean_filename = decoded.encode('euc-kr').decode('euc-kr')

        filename = self.__sanitize_string(korean_filename)

        return filename
    

    def _get_filename(self, item):
        parsed_url = urlparse(item)
        filename = os.path.basename(unquote(parsed_url.path))
        base, extension = os.path.splitext(filename)

        return base, extension
    

    def _process_item(self, item):
        if isinstance(item, list) and len(item) == 2:
            url, filename = item[0], item[1]
        else:
            url, filename = item, self._get_filename(item)

        return url, filename
    
    
    def _download_logic(self, filename, uri, dirs, post_date, loc, cert_bool):
        user_agent = InitUserAgent().get_user_agent()
        
        try:
            with Progress() as progress:
                process = subprocess.Popen([
                            'aria2c', '-d', dirs, 
                            '-c', 
                            '-j', '2', 
                            '-o', filename, uri,
                            '--continue',
                            '--download-result=full',
                            f'--check-certificate={cert_bool}',
                            '-U', user_agent],
                            stdout=subprocess.PIPE,
                            encoding='utf-8',
                            text=True)
                
                task = progress.add_task("Downloading...", total=100)
                
                for line in process.stdout:
                    parts = line.split()
                    if len(parts) >=3 and parts[1].endswith('%)'):
                        progress.update(task, advance=int(re.search(r'\((\d+)%\)', parts[1]).group(1)))
                    if 'Download complete' in line:
                        progress.update(task, completed=100)

            if os.path.exists(dirs + '/' + filename) and post_date is not None:
                utc = pytz.timezone(self._location(loc))
                dt = post_date
                dt = utc.localize(dt)
                timestamp = int(dt.timestamp())
                os.utime(dirs + '/' + filename, (timestamp, timestamp))
                os.utime(dirs, (timestamp, timestamp))
        except requests.exceptions.SSLError:
            print("[Status] SSL Error. Skipping...")
        except requests.exceptions.HTTPError:
            print("[Status] HTTP Error. Skipping...")
        except requests.exceptions.ConnectionError:
            print("[Status] Connection Error. Skipping...")


    def downloader(self, payload):
        img_list, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )
        
        for img in img_list:
            # get url and separate the filename as a new variable
            base, extension = self._get_filename(img)
            img_name = self._encode_kr(base + extension)

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            if os.path.exists(dirs + '/' + img_name) and not os.path.exists(dirs + '/' + img_name + '.aria2'):
                print("[Status] This file already exists. Skipping...")
                continue

                
            self._download_logic(img_name, img, dirs, post_date, loc, "true")


    def downloader_naver(self, payload):
        img_list, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )

        duplicate_counts = {}
        for img in img_list:
            base, extension = self._get_filename(img)
            img_name = self._encode_kr(base + extension)
            img_ext = img_name.split('.')[-1]

            if img_name in duplicate_counts:
                duplicate_counts[img_name] += 1
                img_name = f"{img_name.split('.')[0]} ({duplicate_counts[img_name]}).{img_ext}"
            else:
                duplicate_counts[img_name] = 0

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            if os.path.exists(dirs + '/' + img_name) and not os.path.exists(dirs + '/' + img_name + '.aria2'):
                print("[Status] This file already exists. Skipping...")
                continue

            self._download_logic(img_name, img, dirs, post_date, loc, "true")


    def downloader_combine(self, payload):
        img_list, dirs, post_date, post_date_short, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.shortDate,
            payload.location,
        )
        
        for img in img_list:
            img_name, img_ext = self._get_filename(img)
            img_name = self._encode_kr(img_name)
            
            if len(img_list) > 1:
                img_name = f'{post_date_short} {img_name} ({img_list.index(img)+1}).{img_ext}'
            else:
                img_name = f'{post_date_short} {img_name}.{img_ext}'

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            if os.path.exists(dirs + '/' + img_name) and not os.path.exists(dirs + '/' + img_name + '.aria2'):
                print("[Status] This file already exists. Skipping...")
                continue

            if 'topstarnews' in img:
                cert_bool = 'false'
            else:
                cert_bool = 'true'

            self._download_logic(img_name, img, dirs, post_date, loc, cert_bool)