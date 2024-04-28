# -*- coding: utf-8 -*-

"""
Module: common_modules.py
Author: danrynr

Description:
This module provides all the common modules used in the project.
"""

import urllib.parse as urlparse
import time
import urllib3
import requests


from bs4 import BeautifulSoup
from client.user import User
from common.logger import Logger


class Requests:
    """Send HTTP requests using requests module"""
    def __init__(self):
        user = User()

        self.user_agent = user.get_user_agent()
        self.certificate = user.get_certificate()
        self.session = requests.Session()
        self.session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': self.user_agent,
             'Accept-Encoding': 'identity',
             'Connection': 'keep-alive'})
        self.retries = 5

    def get(self, url, **kwargs):
        """Send a GET request"""
        exceptions = requests.exceptions
        exceptions2 = urllib3.exceptions
        logger = Logger()
        tries = 1

        while True:
            try:
                self.session.request(url, verify=self.certificate, **kwargs)
            except (exceptions.SSLError,
                    exceptions.HTTPError,
                    exceptions.ConnectionError,
                    exceptions.Timeout,
                    exceptions.TooManyRedirects,
                    exceptions.RequestException,
                    exceptions2.IncompleteRead,
                    exceptions2.ProtocolError) as e:
                logger.info(
                    f"{type(e).__name__}. Retrying... ({tries}/{self.retries})")
                time.sleep(5)
            finally:
                tries += 1
                if tries > self.retries:
                    logger.info(f"Maximum retries of ({self.retries}) exceeded. Skipping...")
                    break


class SiteParser:
    """Parse HTML content using BeautifulSoup"""
    def __init__(self):
        self.soup = None

    def _parse(self, html_cont):
        return BeautifulSoup(html_cont, 'html.parser')


class Encode:
    """Encode percent encoded string to utf-8"""
    def __init__(self):
        self.encode = None

    def _encode_kr(self, string):
        return urlparse.unquote(string, encoding='utf-8')
