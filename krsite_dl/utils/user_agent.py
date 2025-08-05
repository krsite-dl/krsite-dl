"""
Module: user.py
Author: danrynr

Description:
This module provides a User class to get user agent and certificate location.

@class User
    A class that provides user agent and certificate location.
@method get_user_agent
    Returns a random user agent string.
@method get_certificate
    Returns the location of the certificate bundle.
"""
import random
from certifi import where

def random_user_agent():
    """Return a random user agent string."""
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Safari/537.36'
    CHROME_VERSION = (
        '136.0.7103.48',
        '136.0.0.0',
        '135.0.7049.43',
        '134.0.6828.70',
        '133.0.6833.84',
        '133.0.6831.68',
        '133.0.6784.68',
        '132.0.6812.76',
    )

    return UA % random.choice(CHROME_VERSION)

class User:
    """User class to get user agent and certificate location"""

    def __init__(self):
        """Initialize User class"""
        self.ua = random_user_agent()
        self.certificate = where()

    def get_user_agent(self):
        """Return user agent string"""
        return self.ua

    def get_certificate(self):
        """Return certificate location"""
        return self.certificate
