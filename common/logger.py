import logging


class LowercaseLevelFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return super(LowercaseLevelFormatter, self).format(record)


class Logger:
    def __init__(self, log_name):

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        self.console_handler = logging.StreamHandler()
        self.formatter = LowercaseLevelFormatter(
            "[%(name)s][%(levelname)s] %(msg)s"
        )
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

    def log_info(self, msg, *args, **kwargs):
        self.logger.info(f"{msg}", *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.logger.warning(f"{msg}", *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.logger.error(f"{msg}", *args, **kwargs)
