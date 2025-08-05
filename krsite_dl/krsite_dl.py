# -*- coding: utf-8 -*-

"""
Module: krsite_dl.py
Author: danrynr

Description:
This module is the main entry point for the application.
"""

import sys
import importlib

from urllib.parse import urlparse
from .utils.logger import Logger
from .utils.parser import parse_args, get_args
from .extractor_registry import LAZY_EXTRACTOR_MAP
from .downloader.directory import DirectoryHandler
from .downloader.download import DownloadHandler

def check_site(url):
    hostname = urlparse(url).hostname
    logger = Logger('check_site')

    module_path_to_import = None
    for site_key, module_path in LAZY_EXTRACTOR_MAP.items():
        if site_key in hostname:
            module_path_to_import = module_path
            break # Found our match

    if module_path_to_import:
        try:
            extractor_module = importlib.import_module(module_path_to_import)
            result = extractor_module.get_data(url)
            if result is not None:
                yield from result  
        except ImportError:
            logger.log_error(f"Could not import module: {module_path_to_import}")
        except Exception as e:
            logger.log_error(f"An error occurred with module {module_path_to_import}: {e}")
    else:
        logger.log_warning(f"No extractor found for hostname: {hostname}")

def main():
    """Main function"""
    logger = Logger('krsite_dl')

    parse_args()
    args = get_args()

    directory = DirectoryHandler()
    download = DownloadHandler()

    try:
        if args.a:
            with open(args.a, 'r') as f:
                for line in f:
                    if line.startswith(('#', ';', ']')):
                        continue
                    for x in check_site(line.strip()):
                        download.downloader(directory.handle_directory(x))
    except FileNotFoundError:
        logger.log_warning(f"File not found: {args.a}")
    except KeyboardInterrupt:
        logger.log_warning("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    if args.a or args.url:
        try:
            for url in args.url:
                for x in check_site(url):
                    download.downloader(directory.handle_directory(x))                 
                    
        except AttributeError as e:
            logger.log_error(f"Attribute Error: {e}")
        except IndexError as e:
            logger.log_error(f"Index Error: {e}")
        except KeyboardInterrupt:
            logger.log_warning(
                "KeyboardInterrupt detected. Exiting gracefully.")
            sys.exit(0)


if __name__ == '__main__':
    main()
