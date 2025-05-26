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

from fake_useragent import UserAgent
from certifi import where


class User:
    """User class to get user agent and certificate location"""

    def __init__(self):
        self.ua = UserAgent(
            browsers=['firefox', 'chrome'],
            os=['windows', 'linux', 'macos'],
            min_percentage=1.3).random
        self.certificate = where()

    def get_user_agent(self):
        """Return user agent string"""
        return self.ua

    def get_certificate(self):
        """Return certificate location"""
        return self.certificate
