from fake_useragent import UserAgent

class InitUserAgent:
    def __init__(self):
        self.ua = UserAgent(
            browsers=['firefox', 'chrome'], 
            os=['windows', 'linux', 'macos'], 
            min_percentage=1.3).random

    def get_user_agent(self):
        return self.ua