import requests
import time

from bs4 import BeautifulSoup
from client.user import User
from common.logger import Logger

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


    def get(self, url, retries=5, **kwargs):
        self.retries = retries
        exceptions = requests.exceptions
        logger = Logger()
        tries = 1

        while True:
            try:
                self.session.request(url, verify=self.certificate, **kwargs)
            except (exceptions.ConnectionError, exceptions.Timeout, exceptions.HTTPError) as e:
                logger.info(f"{type(e).__name__}. Retrying... ({tries}/{self.retries})")
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
    

class SeleniumParser:
    webdriver_options = Options()
    select_by = By()

    def __init__(self):
        self.webdriver_options.add_argument('--headless')
        self.webdriver = wd.Chrome(options=self.webdriver_options)


    def _requests(self, url):
        self.webdriver.get(url)
        return self.webdriver
    

    def find_element(self, el, value):
        return self.webdriver.find_element(el, value)
    

    def find_elements(self, el, value):
        return self.webdriver.find_elements(el, value)
    

    def get_by(self, attribute):
        return getattr(self.select_by, attribute)
    

    def click(self, el):
        return el.click()
    

    def wait(self, el, timeout):
        return WebDriverWait(el, timeout)
    

    def visibility_of(self, el):
        return EC.visibility_of(el)
    

    def presence_of_element_located(self, el):
        return EC.presence_of_element_located(el)