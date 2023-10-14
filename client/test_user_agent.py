import unittest

from user_agent import InitUserAgent

class TestInitUserAgent(unittest.TestCase):
    def setUp(self):
        self.ua = InitUserAgent()

    def test_get_user_agent(self):
        user_agent = self.ua.get_user_agent()
        print(f"User-Agent: {user_agent}")
        self.assertIsInstance(user_agent, str)
        

if __name__ == '__main__':
    unittest.main()