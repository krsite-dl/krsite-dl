import argparse
import configparser
import sys
from rich import print
from urllib.parse import urlparse
from common.logger import Logger
import lazy_import  

# Reading settings from config file
config = configparser.ConfigParser()
config.read('krsite-dl.config')
if config.has_section('Settings'):
    destination_dir = config['Settings']['base_dir']
else:
    destination_dir = '.'

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='*',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
# parser.add_argument("-ai", type=str, help="text file containing image urls")
parser.add_argument("--no-windows-filenames", action="store_true", help="(default=False) krsite-dl will keep the original filenames of the images. This includes filenames that are not allowed in Windows OS.")
parser.add_argument("-d", "--destination", default=destination_dir, type=str, help="The destination path for the downloaded file (unnecessary if you have `krsite-dl.config` unless you want to override the default download path)")
parser.add_argument("-s", "--select", action="store_true", default=False, help="Select which images to download from the list of images gathered from each url. You probably not wanna use this if you're downloading multiple site URLs at once cause it will prompt you for each url.")
args = parser.parse_args()

sitename = ''

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


def main():
    logger = Logger("krsite-dl")
    try:
        if args.a:
            with open(args.a, 'r') as f:
                for line in f:
                    if line[0] == '#' or line[0] == ';' or line[0] == ']':
                        continue
                    elif line != '\n':
                        check_site(line.strip())                        
    except FileNotFoundError:
        print("File not found: %s" % args.a)
    except KeyboardInterrupt:
        print("\r", end="")
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    # if args.ai:
    #     print("*Direct image url mode")
    #     with open(args.ai, 'r') as f:
    #         for line in f:
    #             if line[0] == '#' or line[0] == ';' or line[0] == ']':
    #                 continue
    #             elif line != '\n':
    #                 try:
    #                     direct.from_direct(line)
    #                 except FileNotFoundError:
    #                     logger.log_warning("File not found: %s" % args.ai)
    #                 except IndexError as e:
    #                     logger.log_error("Index Error: %s" % e)
    #                     print("Index Error: %s" % e)
    #                 except KeyboardInterrupt:
    #                     logger.log_warning("KeyboardInterrupt detected. Exiting gracefully.")
    #                     sys.exit(0)
    if args.a or args.url:
        try:
            for url in args.url:
                check_site(url)

        except AttributeError as e:
            logger.log_error("Attribute Error: %s" % e)
        except IndexError as e:
            logger.log_error("Index Error: %s" % e)
            print("Index Error: %s" % e)
        except KeyboardInterrupt:
            logger.log_warning("KeyboardInterrupt detected. Exiting gracefully.")
            sys.exit(0)


if __name__ == '__main__':
    main()