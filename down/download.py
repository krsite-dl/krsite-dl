import requests
import urllib3
import os
import re
import time
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
    duplicate_counts = {}
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds

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
        # check if its url or not
        if not item.startswith('http'):
            base, x = os.path.splitext(item)
            return base, x

        parsed_url = urlparse(item)
        filename = os.path.basename(unquote(parsed_url.path))
        base, x = os.path.splitext(filename)
        # print(base, x)
        return base, x

    def _process_item(self, item):
        if isinstance(item, (list, dict, tuple)) and len(item) == 2:
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
            self.logger.log_warning(
                f"File: {filename} already exists. Skipping...")
            return True

    def _session(self):
        session = requests.Session()
        session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': self.user_agent,
             'Accept-Encoding': 'identity',
             'Connection': 'keep-alive'})
        return session

    def _retry_request(self, url, certificate, session, r_headers=None):
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = session.get(url, verify=certificate, headers=r_headers, stream=True)
                return response
            except (requests.exceptions.SSLError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.TooManyRedirects,
                    requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.RequestException,
                    urllib3.exceptions.IncompleteRead,
                    urllib3.exceptions.ProtocolError) as e:
                self.logger.log_error(
                    f"{type(e).__name__}. Retrying... ({attempt}/{self.MAX_RETRIES})")
                time.sleep(self.RETRY_DELAY)
                session.close()
                session = self._session()

        return None  # Return None if maximum retries exceeded

    def _download_logic(self, medialist, dirs, option=None, custom_headers=None):
        self.successful_requests = 0
        self.total_requests = len(medialist)
        self.skipped_due_to_existence = 0
        self.error_requests = 0

        for url in medialist:
            # print out information about the source and filename
            if kr.args.verbose:
                self.logger.log_info(f"{url}")
        
            match option:
                case "naverpost":
                    if filename in self.duplicate_counts:
                        self.duplicate_counts[filename] += 1
                        filename = f"{filename} ({self.duplicate_counts[filename]})"
                    else:
                        self.duplicate_counts[filename] = 0
                case "naverblog":
                    if isinstance(url, tuple):
                        url, filename = self._process_item(url)
                    else:
                        base, ext = self._get_filename(url)
                        filename = self._encode_kr(base)
                        if filename in self.duplicate_counts:
                            self.duplicate_counts[filename] += 1
                            filename = f"{filename} ({self.duplicate_counts[filename]})"
                        else:
                            self.duplicate_counts[filename] = 0
                case "combine":
                    if len(medialist) > 1:
                        filename = f'{filename} ({medialist.index(url)+1})'
                case "defined":
                    # get url and separate the filename as a new variable
                    # each list has a url with its predefined filename
                    if isinstance(url, tuple):
                        url, name = self._process_item(url)
                        name = self._encode_kr(name)
                        base, ext = self._get_filename(name)
                        filename = base
                    else:
                        # split the filename and extension from url
                        base, ext = self._get_filename(url)
                        # encode the filename to appropriate format
                        filename = self._encode_kr(base)

            # request
            certificate = self.certificate
            response = self._retry_request(url, certificate, self.session, custom_headers)

            if response is None:
                self.logger.log_error(f"Max retries exceeded. Skipping...")
                continue

            # Check if it returns code 4xx or 5xx
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                self.error_requests += 1
                if 400 <= response.status_code < 500:
                    self.logger.log_error(
                        f"Client Error Code {response.status_code} - {response.reason}")
                    continue

                if 500 <= response.status_code:
                    self.logger.log_error(
                        f"Server Error Code {response.status_code} - {response.reason}")
                    continue


            # get headers
            headers = response.headers
            content_type = headers.get('content-type')
            content_length = headers.get('content-length')
            last_modified = headers.get('last-modified')
            content_disposition = headers.get('content-disposition')

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

            content_length = int(content_length)  # get the content length

            # if filename is provided on content_disposition, use it
            if content_disposition is not None:
                filename = content_disposition.split('filename=')[1].strip('"')
                filename = self.__sanitize_string(filename)
                base, ext = self._get_filename(filename)
                filename = self._encode_kr(base)

            file_extension = file_extensions.get(content_type, '.jpg')

            # check if file already exists
            if self._file_exists(dirs, f"{filename}{file_extension}"):
                self.skipped_due_to_existence += 1
                continue

            self.successful_requests += 1

            self.logger.log_info(f"filename: {filename}{file_extension}")
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
                        task = prog.add_task(
                            "Downloading...", total=content_length)
                        for chunk in response.iter_content(chunk_size=4194304):
                            current_size += len(chunk)
                            f.write(chunk)
                            prog.update(task, completed=current_size)

                os.rename(file_part, file_real)

                # convert GMT to local time for last_modified
                # Thu, 07 Dec 2023 02:01:31 GMT
                if last_modified is not None:
                    dt = email.utils.parsedate_to_datetime(last_modified)
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    timestamp = int(dt.timestamp())
                    os.utime(file_real, (timestamp, timestamp))
                    os.utime(dirs, (timestamp, timestamp))
                continue
        self.duplicate_counts.clear()
        self.logger.log_info(
            f"Downloaded {self.successful_requests}/{self.total_requests} file(s) in this session")
        if self.skipped_due_to_existence > 0:
            self.logger.log_info(
                f"Skipped {self.skipped_due_to_existence} file(s) due to existence")
        if self.error_requests > 0:
            self.logger.log_info(
                f"Failed to download {self.error_requests} file(s) due to errors"
            )

    def downloader(self, payload):
        medialist, dirs, option, r_headers = (
            payload.media,
            payload.directory,
            payload.option,
            payload.custom_headers
        )

        if kr.args.select:
            medialist = self._media_selector(medialist)

        self._download_logic(medialist, dirs, option=option, custom_headers=r_headers)
        self.session.close()
