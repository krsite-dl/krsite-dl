import requests
import os
import re
import time
import pytz
import certifi
import email.utils

from datetime import timezone
from rich.progress import Progress
from urllib.parse import unquote, urlparse
from client.user_agent import InitUserAgent
import krsite_dl as kr

class DownloadHandler():
    def __init__(self):
        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]'
        self.session = self._session()
        self.certificate = self._cert()

    
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
        decoded = unquote(img_name)

        if '%EC' in decoded or '%EB' in decoded:
            korean_filename = decoded.encode('utf-8')
        else:
            korean_filename = decoded.encode('euc-kr', errors='ignore')

        filename = self.__sanitize_string(korean_filename.decode('euc-kr'))

        return filename
    

    def _get_filename(self, item):
        parsed_url = urlparse(item)
        filename = os.path.basename(unquote(parsed_url.path))
        base, x = os.path.splitext(filename)
        # print(base, x)
        return base, x
    

    def _process_item(self, item):
        if isinstance(item, list) and len(item) == 2:
            url, filename = item[0], item[1]
        else:
            url, filename = item, self._get_filename(item)

        return url, filename
    

    def _extension_to_mime(self, ext):
        extensions = {
            '.jpg' or '.jpeg': '.jpg',
            '.JPG' or '.JPEG': '.jpg',
            '.png': '.png',
            '.PNG': '.png',
            '.gif': '.gif',
            '.GIF': '.gif',
            '.webp': '.webp',
            '.WEBP': '.webp',
        }
        return extensions.get(ext, '.jpg')


    def _session(self):
        session = requests.Session()
        session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': InitUserAgent().get_user_agent(), 
             'Accept-Encoding': 'identity', 
             'Connection': 'keep-alive'})
        return session
    

    def _cert(self):
        return certifi.where() # get the path of cacert.pem
    
    
    def _download_logic(self, filename, uri, dirs, post_date, loc):
        try:
            certificate = self.certificate
            response = self.session.get(uri, verify=certificate, stream=True)
            

            # get headers
            headers = response.headers
            content_type = headers.get('content-type')
            content_length = headers.get('content-length')
            last_modified = headers.get('last-modified')

            # get file extension
            if content_type is None:
                pass
            else:
                file_extensions = {
                    'image/jpeg': '.jpg',
                    'image/png': '.png',
                    'image/gif': '.gif',
                    'image/webp': '.webp',
                }

            content_length = int(content_length)

            file_extension = file_extensions.get(content_type, '.jpg')

            file_part = os.path.join(dirs, f"{filename}{file_extension}.part")
            file_real = os.path.join(dirs, f"{filename}{file_extension}")
            try:
                current_size = os.path.getsize(file_part)
            except FileNotFoundError:
                current_size = 0

            if current_size < content_length:
            # download file
                with open(file_part, 'wb') as f:
                    with Progress() as prog:
                        task = prog.add_task("Downloading...", total=content_length)
                        for chunk in response.iter_content(chunk_size=20480):
                            current_size += len(chunk)
                            f.write(chunk)
                            prog.update(task, completed=current_size)


                os.rename(file_part, file_real)

                #convert GMT to local time for last_modified
                #Thu, 07 Dec 2023 02:01:31 GMT
                if last_modified is not None:
                    dt = email.utils.parsedate_to_datetime(last_modified)
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    timestamp = int(dt.timestamp())
                    os.utime(file_real, (timestamp, timestamp))
                    os.utime(dirs, (timestamp, timestamp))
                else:
                    utc = pytz.timezone(self._location(loc))
                    dt = post_date
                    dt = utc.localize(dt)
                    timestamp = int(dt.timestamp())
                    os.utime(file_real, (timestamp, timestamp))
                    os.utime(dirs, (timestamp, timestamp))
        except requests.exceptions.SSLError:
            print("[Status] SSL Error. Skipping...")
        except requests.exceptions.HTTPError:
            print("[Status] HTTP Error. Skipping...")
        except requests.exceptions.ConnectionError:
            # retry 3 times using its session
            print("[Status] Connection Error. Retrying...")
            try:
                for i in range(3):
                    print(f"[Status] Retry {i+1}...")
                    self._download_logic(filename, uri, dirs, post_date, loc)
                    break
            except requests.exceptions.ConnectionError:
                print("[Status] Max retries exceeded. Skipping...")


    def downloader(self, payload):
        img_list, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )
        
        for img in img_list:
            # get url and separate the filename as a new variable
            base, ext = self._get_filename(img)
            filename = self._encode_kr(base)
            ext = self._extension_to_mime(ext)

            img_name = f"{filename}{ext}"

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            # and not os.path.exists(dirs + '/' + img_name + '.aria2')
            if os.path.exists(dirs + '/' + img_name):
                print("[Status] This file already exists. Skipping...")
                continue

                
            self._download_logic(filename, img, dirs, post_date, loc)


    def downloader_naver(self, payload):
        img_list, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )

        duplicate_counts = {}
        for img in img_list:
            base, ext = self._get_filename(img)
            filename = self._encode_kr(base)
            ext = self._extension_to_mime(ext)
        
            if filename in duplicate_counts:
                duplicate_counts[filename] += 1
                img_name = f"{filename} ({duplicate_counts[filename]}{ext})"
            else:
                duplicate_counts[filename] = 0
                img_name = f"{filename}{ext}"

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            if os.path.exists(dirs + '/' + img_name):
                print("[Status] This file already exists. Skipping...")
                continue

            self._download_logic(filename, img, dirs, post_date, loc)


    def downloader_combine(self, payload):
        img_list, dirs, post_date, post_date_short, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.shortDate,
            payload.location,
        )
        
        for img in img_list:
            img_name, ext = self._get_filename(img)
            filename = self._encode_kr(img_name)
            ext = self._extension_to_mime(ext)
            
            if len(img_list) > 1:
                img_name = f'{filename} ({img_list.index(img)+1}){ext}'
            else:
                img_name = f'{filename}{ext}'

            print("[Source URL] %s" % img)
            print("[Image Name] %s" % img_name)

            if os.path.exists(dirs + '/' + img_name):
                print("[Status] This file already exists. Skipping...")
                continue

            self._download_logic(filename, img, dirs, post_date, loc)
        
        self.session.close()