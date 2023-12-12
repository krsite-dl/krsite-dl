import requests
from client.user import User
from bs4 import BeautifulSoup
from common.logger import Logger

class SiteRequests:
    def __init__(self):
        user = User()

        self.user_agent = user.get_user_agent()
        self.certificate = user.get_certificate()
        self.session = requests.Session()
        self.session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': self.user_agent, 
             'Accept-Encoding': 'identity', 
             'Connection': 'keep-alive'})


    def get(self, url):
        logger = Logger()
        try:
            self.session.get(url, verify=self.certificate)
        except ConnectionError:
            logger.log_error("Connection error!")
        

class SiteParser:
    def __init__(self):
        self.soup = None

    
    def _parse(self, html):
        return BeautifulSoup(html, 'html.parser')