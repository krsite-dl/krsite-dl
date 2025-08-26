"""
Module: krsite_dl.py
Author: danrynr

Description:
This module is responsible for parsing command line arguments
and reading configuration files for the krsite-dl utility.
"""

import argparse
import configparser
import os
import platform

from importlib_metadata import version, PackageNotFoundError

_args = None


def parse_args():
    """
    Parses command line arguments for the krsite-dl utility.
    Returns an argparse.Namespace object with the parsed arguments.
    """
    global _args
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
    utility_group.add_argument("-v", "--verbose",
                                action="store_true",
                                help="Increase output verbosity")
    utility_group.add_argument("--version",
                                action="store_true",
                                help="Print program version and exit")
    misc_group = parser.add_argument_group("misc")
    misc_group.add_argument("--no-windows-filenames",
                            action="store_true",
                            help="(default=False) krsite-dl will not sanitize filenames")
    _args = parser.parse_args()

    if _args.version:
        try:
            print(f"krsite-dl on {version('krsite-dl')}")
        except PackageNotFoundError:
            print("krsite-dl not installed")
        exit()

    _conf_d = search_config()
    if _args.destination:
        pass
    else:
        if _conf_d is None:
            _args.destination = os.path.join(os.path.expanduser('~'), 'Pictures')
        else:
            if _conf_d.get('destination_dir'):
                _args.destination = _conf_d.get('destination_dir')
            if _args.config:
                _args.destination = read_config(_args.config).get('destination_dir')
        if _args.config:
            _args.destination = read_config(_args.config).get('destination_dir')

def get_args():
    """
    Returns the parsed command line arguments.
    If arguments have not been parsed yet, it calls parse_args() first.
    """
    if _args is None:
        raise RuntimeError("Arguments have not been parsed yet. Call parse_args() first.")
    return _args



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
            
    elif platform.system() == "Darwin":
        config_locations = [
            os.path.join(os.path.expanduser('~/Library/Application Support/krsite-dl'),
                         'krsite-dl.conf'),
            os.path.join(os.path.expanduser('~'),
                         'krsite-dl.conf'),
        ]
        for config_location in config_locations:
            if os.path.exists(config_location):
                return read_config(config_location)
