import os
import re
from down.download import DownloadHandler
import krsite_dl as kr

class DirectoryHandler:
    def __init__(self):
        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]' # windows reserved characters


    # sanitize string to remove windows reserved characters
    def __sanitize_string(self, string1, string2, string3 = None):
        if not self.args.no_windows_filenames:
            string1 = re.sub(self.reserved_pattern, '', string1)
            string2 = re.sub(self.reserved_pattern, '', string2)
            if string3: 
                string3 = re.sub(self.reserved_pattern, '', string3)
                return string1, string2, string3
            
        return string1, string2
    

    # create directory if it doesn't exist
    def _create_directory(self, directory_name, *subfolders):
        dirs = os.path.join(self.args.destination, directory_name, *subfolders)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        return dirs
    

    # directory handling for press sites / blogs that have distinct topics
    def handle_directory(self, img_list, title=None, post_date=None, post_date_short=None, loc=None, directory_name=None):
        title, directory_name = self.__sanitize_string(title, directory_name)

        if title and post_date_short:
            dirs = self._create_directory(directory_name, f'{post_date_short} {title}')
        else:
            dirs = self._create_directory(directory_name)

        # if self.args.ai:
        #     download_handler_alt(img_list, dirs, post_date, loc)
        # else:
        #     download_handler(img_list, dirs, post_date, loc)
        DownloadHandler().downloader(img_list, dirs, post_date, loc)


    # directory handling for press sites / blogs that don't have distinct topics (e.g. news / random topics)
    def handle_directory_alternate(self, img_list, title = None, post_date = None, post_date_short = None, loc = None, directory_name = None):
        title, directory_name = self.__sanitize_string(title, directory_name)

        if title and post_date_short:
            dirs = self._create_directory(directory_name, post_date_short, title)
        else:
            dirs = self._create_directory(directory_name)

        DownloadHandler().downloader(img_list, dirs, post_date, loc)


    # directory handling for naver blogs
    def handle_directory_naver(self, img_list, title = None, post_date = None, post_date_short = None, series = None, post_writer = None, directory_name = None):
        title, post_writer, series = self.__sanitize_string(title, post_writer, series)

        if title and post_date_short and series:
            dirs = self._create_directory(directory_name, post_writer, series, f'{post_date_short} {title}')
        else:
            dirs = self._create_directory(directory_name, 'krsite-dl')

        DownloadHandler().downloader_naver(img_list, dirs, post_date)


    # directory handling for news1 (news1.kr). Create a single directory, instead of multiple directories for each article we use the name of the article as image name
    def handle_directory_combine(self, img_list, title=None, post_date=None, post_date_short=None, loc=None, directory_name=None):
        title, directory_name = self.__sanitize_string(title, directory_name)

        dirs = self._create_directory(directory_name)

        DownloadHandler().downloader_combine(img_list, dirs, post_date, post_date_short, title, loc)