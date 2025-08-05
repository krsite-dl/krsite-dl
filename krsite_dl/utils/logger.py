"""
Module: logger.py
Author: danrynr

Description:
This module provides a custom logger that formats log messages with lowercase level names and optional tags.

@class LowercaseLevelFormatter:
    A custom logging formatter that converts log level names to lowercase and formats messages with optional tags.
    It also ensures that optional fields exist to prevent KeyError.

@class Logger:
    A custom logger that initializes a logger with a specific name and optional extractor name.
    It provides methods to log messages at different levels (info, warning, error) with optional custom tags.
    It also includes a method to log extractor information with structured output.
"""

import logging

class LowercaseLevelFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        # Ensure optional fields exist to prevent KeyError
        record.tag = getattr(record, "tag", "").lower().replace(" ", "")
        record.custom_tag = getattr(record, "custom_tag", "")
        return super().format(record) 

class Logger:
    """Custom logger"""
    def __init__(self, log_name, extractor_name=None):
        self.extractor_name = extractor_name or ""
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        self.console_handler = logging.StreamHandler()
        self.formatter = LowercaseLevelFormatter(
            "[%(name)s"  # log_name like "extractor"
            "%(tag)s"    # extractor_name if set
            "][%(levelname)s]"
            "%(custom_tag)s %(msg)s"
        )
        self.console_handler.setFormatter(self.formatter)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)

    def _log(self, level, msg, custom_tag=None, *args, **kwargs):
        extra = {
            "tag": f"][{self.extractor_name}" if self.extractor_name else "",
            "custom_tag": f"[{custom_tag}]" if custom_tag else "",
        }
        self.logger.log(level, msg, extra=extra, *args, **kwargs)

    def log_info(self, msg, custom_tag=None, *args, **kwargs):
        self._log(logging.INFO, msg, custom_tag, *args, **kwargs)

    def log_warning(self, msg, custom_tag=None, *args, **kwargs):
        self._log(logging.WARNING, msg, custom_tag, *args, **kwargs)

    def log_error(self, msg, custom_tag=None, *args, **kwargs):
        self._log(logging.ERROR, msg, custom_tag, *args, **kwargs)

    def log_extractor_info(self, *args):
        """Log extractor information"""
        a = len(args)
        if a >= 3:
            *extra, title, date, content = args
        if a == 2:
            extra = []
            title, content = args
            date = None
        for line in extra:
            self.log_info(line)

        self.log_info(f"Title: {title}")
        self.log_info(f"Date: {date or 'N/A'}")
        self.log_info(f"Content: {len(content)} media(s)")
        