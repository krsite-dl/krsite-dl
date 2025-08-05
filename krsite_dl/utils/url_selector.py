"""
Module: url_selector.py
Author: danrynr

Description:
This module provides a function to select URLs from a list using the inquirer library.
It prompts the user to select which URLs they want to download from.

@function select_url
    Prompts the user to select URLs from a provided list.
    Returns the selected URLs.
"""

import inquirer
import sys
from .logger import Logger

logger = Logger('url_selector')

def select_url(img_list):
    try:
        questions = [
            inquirer.Checkbox("url",
                              message="Select which url to download from:",
                              choices=img_list, default=img_list,
                              )
        ]

        answer = inquirer.prompt(questions)
        logger.log_info("Selected URLs to download: %s" % len(answer["url"]))

        return answer["url"]
    except (TypeError):
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)
