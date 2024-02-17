
import argparse
import configparser
import os
import platform
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from rich.progress import Progress
import lazy_import
from common.logger import Logger


class ConfigManager:
    @staticmethod
    def read_config(fpath):
        if not os.path.exists(fpath):
            return {}
        config = configparser.ConfigParser()
        config.read(fpath)
        if config.has_section('Settings'):
            return dict(config.items('Settings'))
        return {}

    @staticmethod
    def search_config():
        config_locations = {
            "Windows": [
                os.path.join(os.getenv('APPDATA'), 'krsite-dl.conf'),
                os.path.join(os.getenv('USERPROFILE'), 'krsite-dl', 'krsite-dl.conf'),
                os.path.join(os.getenv('USERPROFILE'), 'krsite-dl.conf'),
            ],
            "Linux": [
                '/etc/krsite-dl.conf',
                os.path.join(os.path.expanduser('~/.config/krsite-dl'), 'krsite-dl.conf'),
                os.path.join(os.path.expanduser('~'), 'krsite-dl.conf'),
            ]
        }
        system = platform.system()
        for location in config_locations.get(system, []):
            if os.path.exists(location):
                return ConfigManager.read_config(location)
        return {}


class SiteHandler:
    def __init__(self):
        self.sites_available = lazy_import.imported_modules

    def check_site(self, url):
        hostname = urlparse(url).hostname
        for module_name, module in self.sites_available.items():
            if hasattr(module, 'SITE_INFO'):
                site_info = module.SITE_INFO
                if isinstance(site_info.hostname, (str, list)) and hostname in site_info.hostname:
                    print(f"[cyan]From {module_name}[/cyan]")
                    print(f"[magenta]Url: {url}[/magenta]")
                    module.get_data(url)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs='*', type=str, help="valid news/blog url")
    parser.add_argument("-c", "--config", type=str, help="File path to your config file")
    parser.add_argument("-a", type=str, help="Text file containing site urls")
    parser.add_argument("-d", "--destination", type=str, help="The destination path for the downloaded file.")
    parser.add_argument("-s", "--select", action="store_true", default=False, help="Select which images to download from each url.")
    parser.add_argument("--no-windows-filenames", action="store_true", help="(default=False) krsite-dl will not sanitize filenames")
    parser.add_argument("--parallel", type=int, default=5, help="Number of parallel downloads")
    return parser.parse_args()


def main():
    args = parse_arguments()
    logger = Logger("krsite-dl")
    config_manager = ConfigManager()
    site_handler = SiteHandler()

    # Load configuration
    config = config_manager.search_config() or {}
    destination_dir = args.destination or config.get('destination_dir', os.path.join(os.path.expanduser('~'), 'Pictures'))

    # Setup ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = []

        def download_site(url):
            try:
                site_handler.check_site(url)
            except Exception as e:
                logger.log_warning(f"An error occurred while downloading {url}: {e}")

        if args.a:
            with open(args.a, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith(('#', ';', ']')):
                        continue
                    futures.append(executor.submit(download_site, line.strip()))

        for url in args.url:
            futures.append(executor.submit(download_site, url))

        # Progress bar
        with Progress() as progress:
            task = progress.add_task("[cyan]Downloading...", total=len(futures))
            for future in futures:
                result = future.result()  # Blocks until the future is done
                progress.update(task, advance=1)

    print(f"Download destination: {destination_dir}")


if __name__ == '__main__':
    main()
