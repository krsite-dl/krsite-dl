from fake_useragent import UserAgent
from certifi import where

class User:
    def __init__(self):
        self.ua = UserAgent(
            browsers=['firefox', 'chrome'], 
            os=['windows', 'linux', 'macos'], 
            min_percentage=1.3).random
        self.certificate = where()


    def get_user_agent(self):
        return self.ua
    

    def get_certificate(self):
        return self.certificate