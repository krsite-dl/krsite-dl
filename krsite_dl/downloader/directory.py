"""
Module: krsite_dl.py
Author: danrynr

Description:
This module is responsible for handling directory creation.
"""

import os
import re

from utils.data_structure import DownloadPayload
from utils.logger import Logger
from utils.parser import get_args


class DirectoryHandler:
    logger = Logger('directory')

    def __init__(self):
        self.args = get_args()
        self.reserved_pattern = r'[\\/:*?"<>|]'  # windows reserved characters

    # sanitize string to remove windows reserved characters

    def __sanitize_string(self, *strings):
        sanitized_strings = []
        for string in strings:
            if not self.args.no_windows_filenames:
                string = re.sub(self.reserved_pattern, '', string)
                string = re.sub(r'\.+?$', '', string)  # remove trailing dots
            sanitized_strings.append(string)
        return sanitized_strings

    # create directory if it doesn't exist

    def _create_directory(self, directory_format):
        directory_format = [str(element) for element in directory_format]
        dirs = os.path.join(self.args.destination, *directory_format)
        if not os.path.exists(dirs):
            self.logger.log_warning(f"Directory not exists")
            self.logger.log_info(f"Creating directory: {dirs}")
            os.makedirs(dirs)
        return dirs

    def handle_directory(self, payload):
        directory_format, media_list, option, c_headers = (
            payload.directory_format,
            payload.media,
            payload.option,
            payload.custom_headers
        )

        # sanitize directory name
        directory_format = self.__sanitize_string(*directory_format)
        # create directory
        dirs = self._create_directory(directory_format)

        download_payload = DownloadPayload(
            media=media_list,
            directory=dirs,
            option=option,
            custom_headers=c_headers
        )

        return download_payload
