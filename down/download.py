import requests
import os
import re
import time
import pytz
import email.utils

from datetime import timezone
from rich.progress import Progress
from urllib.parse import unquote, urlparse
from client.user import User
from common.url_selector import select_url
from common.logger import Logger

import krsite_dl as kr

class DownloadHandler():
    logger = Logger("downloader")
    def __init__(self):
        user = User()

        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]'
        self.user_agent = user.get_user_agent()
        self.certificate = user.get_certificate()
        self.session = self._session()

    
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
    

    def _media_selector(self, img_list):
        logger = Logger("media_selector")
        logger.log_info("Selecting images to download...")
        selected = select_url(img_list)

        if not selected:
            logger.log_info("No images selected.")
        return selected
    

    def _file_exists(self, dirs, filename):
        path = os.path.join(dirs, filename)
        if os.path.exists(path):
            self.logger.log_warning(f"File {filename} already exists. Skipping...")
            return True


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
            {'User-Agent': self.user_agent, 
             'Accept-Encoding': 'identity', 
             'Connection': 'keep-alive'})
        return session
    
    
    def _download_logic(self, filename, url, dirs, post_date, loc):
        max_retries = 3
        retry_delay = 5 #seconds

        for attempt in range(1, max_retries+1):
            try:
                certificate = self.certificate
                response = self.session.get(url, verify=certificate, stream=True)
                

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
                        with Progress(refresh_per_second=1) as prog:
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
                    break
            except requests.exceptions.SSLError:
                self.logger.log_error(f"SSL Error. Skipping...")
                break
            except requests.exceptions.HTTPError:
                self.logger.log_error(f"HTTP Error. Skipping...")
                break
            except requests.exceptions.ConnectionError:
                # retry 3 times using its session
                if attempt < max_retries:
                    self.logger.log_error(f"Connection Error. Retrying... ({attempt}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    self.logger.log_error(f"Max retries exceeded. Skipping...")
                    break


    def downloader(self, payload):
        medialist, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )

        if kr.args.select:
            urls = self._media_selector(medialist)
        
        for url in urls:
            # get url and separate the filename as a new variable
            base, ext = self._get_filename(url)
            filename = self._encode_kr(base)
            ext = self._extension_to_mime(ext)

            img_name = f"{filename}{ext}"

            self.logger.log_info(f"{url}")
            self.logger.log_info(f"filename: {img_name}")

            if self._file_exists(dirs, img_name):
                continue
                
            self._download_logic(filename, url, dirs, post_date, loc)

        self.session.close()

        
    def downloader_naver(self, payload):
        medialist, dirs, post_date, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.location,
        )

        if kr.args.select:
            urls = self._media_selector(medialist)

        duplicate_counts = {}
        for url in urls:
            base, ext = self._get_filename(url)
            filename = self._encode_kr(base)
            ext = self._extension_to_mime(ext)
        
            if filename in duplicate_counts:
                duplicate_counts[filename] += 1
                img_name = f"{filename} ({duplicate_counts[filename]}{ext})"
            else:
                duplicate_counts[filename] = 0
                img_name = f"{filename}{ext}"

            self.logger.log_info(f"{url}")
            self.logger.log_info(f"filename: {img_name}")

            if self._file_exists(dirs, img_name):
                continue

            self._download_logic(filename, url, dirs, post_date, loc)

        self.session.close()


    def downloader_combine(self, payload):
        medialist, dirs, post_date, post_date_short, loc = (
            payload.media,
            payload.directory,
            payload.date,
            payload.shortDate,
            payload.location,
        )

        if kr.args.select:
            urls = self._media_selector(medialist)
        
        for url in urls:
            img_name, ext = self._get_filename(url)
            filename = self._encode_kr(img_name)
            ext = self._extension_to_mime(ext)
            
            if len(urls) > 1:
                img_name = f'{filename} ({urls.index(url)+1}){ext}'
            else:
                img_name = f'{filename}{ext}'

            self.logger.log_info(f"{url}")
            self.logger.log_info(f"filename: {img_name}")

            if self._file_exists(dirs, img_name):
                continue

            self._download_logic(filename, url, dirs, post_date, loc)
        
        self.session.close()