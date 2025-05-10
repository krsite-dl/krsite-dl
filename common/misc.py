import time

class Misc:
    """Miscellaneous functions"""

    def __init__(self):
        pass

    def get_time(self):
        """Get current time for nonce"""
        self.current_milli_time = int(round(time.time() * 1000))
        return str(self.current_milli_time)