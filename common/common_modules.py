import requests
import time
import urllib.parse as urlparse

from bs4 import BeautifulSoup
from client.user import User
from common.logger import Logger


class Requests:
    def __init__(self):
        user = User()

        self.user_agent = user.get_user_agent()
        self.certificate = user.get_certificate()
        self.session = requests.Session()
        self.session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': self.user_agent,
             'Accept-Encoding': 'identity',
             'Connection': 'keep-alive'})

    def get(self, url, retries=5, **kwargs):
        self.retries = retries
        exceptions = requests.exceptions
        logger = Logger()
        tries = 1

        while True:
            try:
                self.session.request(url, verify=self.certificate, **kwargs)
            except (exceptions.ConnectionError, exceptions.Timeout, exceptions.HTTPError) as e:
                logger.info(
                    f"{type(e).__name__}. Retrying... ({tries}/{self.retries})")
                time.sleep(5)
            finally:
                tries += 1
                if tries > self.retries:
                    logger.info(f"Maximum retries exceeded. Skipping...")
                    break


class SiteParser:
    def __init__(self):
        self.soup = None

    def _parse(self, html_cont):
        return BeautifulSoup(html_cont, 'html.parser')


class Encode:
    def __init__(self):
        self.encode = None

    def _encode_kr(self, string):
        return urlparse.unquote(string, encoding='utf-8')