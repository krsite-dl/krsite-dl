# -*- coding: utf-8 -*-

"""
Module: krsite_dl.py
Author: danrynr

Description:
This module is the main entry point for the application.
"""

import sys

from urllib.parse import urlparse
from utils.logger import Logger
from lazy_import import imported_modules
from utils.parser import parse_args, get_args
from down.directory import DirectoryHandler
from down.download import DownloadHandler

def check_site(url):
    hostname = urlparse(url).hostname

    sites_available = imported_modules

    for module_name, module in sites_available.items():
        if hasattr(module, 'SITE_INFO'):
            site_info = module.SITE_INFO
            if isinstance(site_info.hostname, str):
                if site_info.hostname in hostname:
                    result = module.get_data(url)
                    if result is not None:
                        yield from result
                    break
                        
            elif isinstance(site_info.hostname, list):
                if any(item in hostname for item in site_info.hostname):
                    result = module.get_data(url)
                    if result is not None:
                        yield from result
                    break

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
