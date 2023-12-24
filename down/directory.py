import krsite_dl as kr
import os
import re

from down.download import DownloadHandler
from common.data_structure import DownloadPayload
from common.logger import Logger

class DirectoryHandler:
    logger = Logger("directory_handler")

    def __init__(self):
        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]' # windows reserved characters    


    # sanitize string to remove windows reserved characters
    def __sanitize_string(self, *strings):
        sanitized_strings = []
        for string in strings:
            if not self.args.no_windows_filenames:
                string = re.sub(self.reserved_pattern, '', string)
            sanitized_strings.append(string)
        return tuple(sanitized_strings)
    

    # create directory if it doesn't exist
    def _create_directory(self, directory_name, *subfolders):
        dirs = os.path.join(self.args.destination, directory_name, *subfolders)
        if not os.path.exists(dirs):
            self.logger.log_warning(f"Directory not exists")
            self.logger.log_info(f"Creating directory: {dirs}")
            os.makedirs(dirs)
        return dirs


    # directory handling for press sites / blogs that have distinct topics
    def handle_directory(self, payload):
        title, post_date_short, post_date, directory_name, loc, media_list = (
            payload.title,
            payload.shortDate,
            payload.mediaDate,
            payload.site, 
            payload.location, 
            payload.media,
        )
        title, directory_name = self.__sanitize_string(title, directory_name)

        if title and post_date_short:
            dirs = self._create_directory(directory_name, f'{post_date_short} {title}')
        else:
            dirs = self._create_directory(directory_name, title)

        # if self.args.ai:
        #     download_handler_alt(img_list, dirs, post_date, loc)
        # else:
        #     download_handler(img_list, dirs, post_date, loc)

        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            date=post_date,
            shortDate=None,
            location=loc,
        )

        DownloadHandler().downloader(download_payload)
    

    # directory handling for press sites / blogs that don't have distinct topics (e.g. news / random topics)
    def handle_directory_alternate(self, payload):
        title, post_date_short, post_date, country_code, directory_name, media_list = (
            payload.title,
            payload.shortDate,
            payload.mediaDate,
            payload.location,
            payload.site,
            payload.media,
        )

        title, directory_name = self.__sanitize_string(title, directory_name)

        if title and post_date_short:
            dirs = self._create_directory(directory_name, post_date_short, title)
        else:
            dirs = self._create_directory(directory_name)

        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            date=post_date,
            shortDate=None,
            location=country_code,
        )

        DownloadHandler().downloader(download_payload)


    # directory handling for naver blogs
    def handle_directory_naver(self, payload):
        title, post_date_short, post_date, directory_name, series, post_writer, country_code, media_list = (
            payload.title,
            payload.shortDate, 
            payload.mediaDate, 
            payload.site, 
            payload.series, 
            payload.writer, 
            payload.location,
            payload.media,
        )

        title, directory_name, post_writer, series = self.__sanitize_string(title, directory_name, post_writer, series)

        if title and post_date_short and series:
            dirs = self._create_directory(directory_name, post_writer, series, f'{post_date_short} {title}')
        else:
            dirs = self._create_directory(directory_name, post_writer, f'{post_date_short} {title}')

        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            date=post_date,
            shortDate=None,
            location=country_code,
        )

        DownloadHandler().downloader_naver(download_payload)

    
    #directory handling for melon
    def handler_directory_melon(self, payload):
        title, post_date_short, post_date, directory_name, country_code, media_list = (
            payload.title,
            payload.shortDate,
            payload.mediaDate,
            payload.site,
            payload.location,
            payload.media,
        )

        title, directory_name = self.__sanitize_string(title, directory_name)

        dirs = self._create_directory(directory_name, title)

        if kr.args.select:
            media_list = self._media_selector(media_list)

        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            date=post_date,
            shortDate=None,
            location=country_code,
        )

        DownloadHandler().downloader(download_payload)

    # directory handling for news1 (news1.kr). Create a single directory, instead of multiple directories for each article we use the name of the article as image name
    def handler_directory_combine(self, payload):
        title, post_date_short, post_date, country_code, directory_name, media_list = (
            payload.title,
            payload.shortDate,
            payload.mediaDate,
            payload.location,
            payload.site,
            payload.media,
        )

        title, directory_name = self.__sanitize_string(title, directory_name)

        dirs = self._create_directory(directory_name, post_date_short)

        if kr.args.select:
            media_list = self._media_selector(media_list)
            
        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            date=post_date,
            shortDate=post_date_short,
            location=country_code,
        )

        DownloadHandler().downloader_combine(download_payload)