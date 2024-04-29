# -*- coding: utf-8 -*-

"""
Module: krsite_dl.py
Author: danrynr

Description:
This module is the main entry point for the application.
"""

import argparse
import configparser
import platform
import os
import sys

from urllib.parse import urlparse
from rich import print
from common.logger import Logger
import lazy_import

parser = argparse.ArgumentParser()
utility_group = parser.add_argument_group("utility")
parser.add_argument("url",
                    nargs='*',
                    type=str,
                    help="valid news/blog url")
utility_group.add_argument("-c", "--config",
                           type=str,
                           help="File path to your config file")
utility_group.add_argument("-a",
                           type=str,
                           help="Text file containing site urls")
utility_group.add_argument("-d", "--destination",
                           type=str,
                           help="The destination path for the downloaded file.")
utility_group.add_argument("-s", "--select",
                           action="store_true",
                           default=False,
                           help="Select which images to download from each url.")
misc_group = parser.add_argument_group("misc")
misc_group.add_argument("--no-windows-filenames",
                        action="store_true",
                        help="(default=False) krsite-dl will not sanitize filenames")
args = parser.parse_args()


def read_config(fpath):
    # Reading settings from config file
    if os.path.exists(fpath):
        config = configparser.ConfigParser()
        config.read(fpath)
        conf = {}
        if config.has_section('Settings'):
            download_dir = config['Settings']['base_dir']
            conf['destination_dir'] = download_dir
        return conf


def search_config():
    if platform.system() == "Windows":
        config_locations = [
            os.path.join(os.getenv('APPDATA'),
                         os.path.expanduser('~'),
                         'krsite-dl.conf'),
            os.path.join(os.getenv('USERPROFILE'),
                         os.path.expanduser('~'),
                         'krsite-dl', 'krsite-dl.conf'),
            os.path.join(os.getenv('USERPROFILE'),
                         os.path.expanduser('~'),
                         'krsite-dl.conf'),
        ]
        for config_location in config_locations:
            if os.path.exists(config_location):
                return read_config(config_location)
    elif platform.system() == "Linux":
        config_locations = [
            '/etc/krsite-dl.conf',
            os.path.join(os.path.expanduser('~/.config/krsite-dl'),
                         'krsite-dl.conf'),
            os.path.join(os.path.expanduser('~'),
                         'krsite-dl.conf'),
        ]
        for config_location in config_locations:
            if os.path.exists(config_location):
                return read_config(config_location)


_conf_d = search_config()
if args.destination:
    pass
else:
    if _conf_d is None:
        args.destination = os.path.join(os.path.expanduser('~'), 'Pictures')
    else:
        if _conf_d.get('destination_dir'):
            args.destination = _conf_d.get('destination_dir')
        if args.config:
            args.destination = read_config(args.config).get('destination_dir')
    if args.config:
        args.destination = read_config(args.config).get('destination_dir')
# print(args.destination)


def check_site(url):
    hostname = urlparse(url).hostname

    sites_available = lazy_import.imported_modules

    for module_name, module in sites_available.items():
        if hasattr(module, 'SITE_INFO'):
            site_info = module.SITE_INFO
            if isinstance(site_info.hostname, str):
                if module.SITE_INFO.hostname in hostname:
                    print(f"[cyan]From {module_name}[/cyan]")
                    print(f"[magenta]Url: {url}[/magenta]")
                    module.get_data(url)
            elif isinstance(site_info.hostname, list):
                if any(item in hostname for item in site_info.hostname):
                    print(f"[cyan]From {module_name}[/cyan]")
                    print(f"[magenta]Url: {url}[/magenta]")
                    module.get_data(url)


"""Main function"""


def main():
    logger = Logger("krsite-dl")

    try:
        if args.a:
            with open(args.a, 'r') as f:
                for line in f:
                    if line.startswith('#', ';', ']'):
                        continue
                    check_site(line.strip())
    except FileNotFoundError:
        logger.log_warning(f"File not found: {args.a}")
    except KeyboardInterrupt:
        logger.log_warning("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    if args.a or args.url:
        try:
            for url in args.url:
                check_site(url)

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
