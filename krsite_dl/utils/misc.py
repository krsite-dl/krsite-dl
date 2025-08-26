"""
Module: misc.py
Author: danrynr

Description:
This module contains miscellaneous utility functions, such as getting the current time in milliseconds.

@class Misc
    A class that provides miscellaneous functions.
@method get_time
    Returns the current time in milliseconds as a string.
"""

import time

class Misc:
    """Miscellaneous functions"""
    @staticmethod
    def get_time():
        """Get current time for nonce"""
        current_milli_time = int(round(time.time() * 1000))
        return str(current_milli_time)