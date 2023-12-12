import logging
from colorlog import ColoredFormatter

class Logger:
    def __init__(self, log_name):

        self.logger = logging.getLogger(log_name)
        self.console_handler = logging.StreamHandler()
        self.formatter = ColoredFormatter(
            "%(log_color)s[%(name)s][%(levelname)s]%(reset)s %(msg)s",
            log_colors={
                'DEBUG': 'cyan,bg_black',
                'INFO': 'cyan,bg_black',
                'WARNING': 'yellow,bg_black',
                'ERROR': 'red,bg_black',
                'CRITICAL': 'red,bg_white',
            },
            reset=True,
            style='%'
        )
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)


    def log_info(self, msg, *args, **kwargs):
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"{msg}", *args, **kwargs)


    def log_warning(self, msg, *args, **kwargs):
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(f"{msg}", *args, **kwargs)


    def log_error(self, msg, *args, **kwargs):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(f"{msg}", *args, **kwargs)