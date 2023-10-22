import argparse
import configparser
import sys
from rich import print
from urllib.parse import urlparse
from extractor import direct, generic
from extractor.kr import dispatch, imbcnews, newsjamm, osen, sbs, sbsnews, mbc, naverpost, navernews, news1, tvreport, topstarnews, kodyssey, tvjtbc, newsen, sportsw, dazedkorea, cosmopolitan, marieclairekorea, lofficielkorea, harpersbazaar, wkorea, elle, vogue, esquirekorea, melon, genie, sbskpop
from extractor.jp import nataliemu, vivi
from extractor.sg import lofficielsingapore

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

    site_dict = {
        # KOREAN SITES
        'KR': [{
            'dispatch.co.kr': ['Dispatch', dispatch.from_dispatch],
            'enews.imbc.com': ['iMBC News', imbcnews.from_imbcnews],
            'mbc.co.kr': ['MBC', mbc.from_mbc],
            'newsjamm.co.kr': ['News Jamm', newsjamm.from_newsjamm],
            'osen.mt.co.kr': ['OSEN', osen.from_osen],
            'osen.co.kr': ['OSEN', osen.from_osen],
            'programs.sbs.co.kr': ['SBS Program', sbs.from_sbs],
            'ent.sbs.co.kr': ['SBS News', sbsnews.from_sbsnews],
            'post.naver.com': ['Naver Post', naverpost.from_naverpost],
            'naver.me': ['Naver Post', naverpost.from_naverpost],
            'news.naver.com': ['Naver News', navernews.from_navernews],
            'news1.kr': ['News1', news1.from_news1],
            'tvreport.co.kr': ['TV Report', tvreport.from_tvreport],
            'topstarnews.net': ['Topstarnews', topstarnews.from_topstarnews],
            'k-odyssey.com': ['K-odyssey', kodyssey.from_kodyssey],
            'tv.jtbc.co.kr': ['JTBC TV', tvjtbc.from_tvjtbc],
            'newsen.com': ['Newsen', newsen.from_newsen],
            'sportsw.kr': ['SportsW', sportsw.from_sportsw],
            'dazedkorea.com': ['Dazed Korea', dazedkorea.from_dazedkorea],
            'cosmopolitan.co.kr': ['Cosmopolitan', cosmopolitan.from_cosmopolitan],
            'marieclairekorea.com': ['Marie Claire Korea', marieclairekorea.from_marieclairekorea],
            'lofficielkorea.com': ["L'officiel Korea", lofficielkorea.from_lofficielkorea],
            'harpersbazaar.co.kr': ["Harper's Bazaar Korea", harpersbazaar.from_harpersbazaar],
            'wkorea.com': ['W Korea', wkorea.from_wkorea],
            'elle.co.kr': ['Elle Korea', elle.from_elle],
            'vogue.co.kr': ['Vogue Korea', vogue.from_vogue],
            'esquirekorea.co.kr': ['Esquire Korea', esquirekorea.from_esquirekorea],
            'melon.com': ['Melon', melon.from_melon],
            'genie.co.kr': ['Genie', genie.from_genie],
            'sbskpop.kr': ['SBS KPOP', sbskpop.from_sbskpop],
        }],
        # JAPANESE SITES
        'JP': [{
            'natalie.mu': ['Natalie 音楽ナタリー', nataliemu.from_nataliemu],
            'vivi.tv': ['ViVi', vivi.from_vivi],
        }],
        # SINGAPOREAN SITES
        'SG': [{
            'lofficielsingapore.com': ["L'officiel Singapore", lofficielsingapore.from_lofficielsingapore],
        }],
        # FALLBACK
        'FALLBACK': [{
            'generic': ['Generic', generic.from_generic],
        }]
    }
    for country in site_dict:
        location = country.upper()
        # print(location)
        for sites in site_dict[country]:
            for site, site_info in sites.items():
                # print(site)
                if site in hostname:
                    print(f"[bold blue]Site name {site}[/bold blue]")
                    print(f"[bold red]Url:[/bold red]\n[italic red]{url}[/italic red]")
                    site_info[1](url, location, site_info[0])
                    return
                

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