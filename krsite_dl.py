import argparse
import configparser
import sys
from rich import print
from urllib.parse import urlparse
from extractor import direct
import lazy_import  

# Reading settings from config file
config = configparser.ConfigParser()
config.read('krsite-dl.config')
if config.has_section('Settings'):
    destination_dir = config['Settings']['base_dir']
else:
    destination_dir = '.'

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='+',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
parser.add_argument("-ai", type=str, help="text file containing image urls")
parser.add_argument("--no-windows-filenames", action="store_true", help="(default=False) krsite-dl will keep the original filenames of the images. This includes filenames that are not allowed in Windows OS.")
parser.add_argument("-d", "--destination", default=destination_dir, type=str, help="The destination path for the downloaded file (unnecessary if you have `krsite-dl.config` unless you want to override the default download path)")
args = parser.parse_args()

sitename = ''

def check_site(url):
    hostname = urlparse(url).hostname

    sites_available = lazy_import.imported_modules

    for module_name, module in sites_available.items():
        # print(module_name)
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

    if args.ai:
        print("*Direct image url mode")
        with open(args.ai, 'r') as f:
            for line in f:
                if line[0] == '#' or line[0] == ';' or line[0] == ']':
                    continue
                elif line != '\n':
                    try:
                        direct.from_direct(line)
                    except FileNotFoundError:
                        print("File not found: %s" % args.ai)
                    except IndexError as e:
                        print("Index Error: %s" % e)
                    except KeyboardInterrupt:
                        print("\r", end="")
                        print("KeyboardInterrupt detected. Exiting gracefully.")
                        sys.exit(0)
    elif args.a or args.url:
        try:
            for url in args.url:
                check_site(url)
        except AttributeError as e:
            print("Attribute Error: %s" % e)
        except IndexError as e:
            print("Index Error: %s" % e)
        except KeyboardInterrupt:
            print("\r", end="")
            print("KeyboardInterrupt detected. Exiting gracefully.")
            sys.exit(0)


if __name__ == '__main__':
    main()