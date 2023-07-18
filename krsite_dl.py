import argparse
import sys
from extractor import direct, generic
from extractor.kr import dispatch, imbcnews, newsjamm, osen, sbs, sbsnews, mbc, naverpost, navernews, news1, tvreport, kodyssey, tvjtbc, newsen, dazedkorea, cosmopolitan, marieclairekorea, lofficielkorea, harpersbazaar, wkorea, elle, vogue
from extractor.jp import nataliemu
from extractor.sg import lofficielsingapore


parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='?',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
parser.add_argument("-ai", type=str, help="text file containing image urls")
parser.add_argument("--no-windows-filenames", action="store_true", help="By default krsite-dl will remove characters that are not allowed in Windows filenames. This option will disable that.")
# parser.add_argument("--force-date", type=str, help="Force a date for the downloaded file. Format: YYYYMMDD HHMMSS")
# parser.add_argument("--board-no", type=int, help="The board number from a site (SBS). For example (https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no=438994) will have a board no of 438994")
parser.add_argument("-d", "--destination", default="/home/biscuits/Pictures", type=str, help="The destination path for the downloaded file")
args = parser.parse_args()

sitename = ''

def check_site(url):
    site_dict = {
        # KOREAN SITES
        'KR': [{
            'dispatch.co.kr': ['Dispatch', dispatch.from_dispatch],
            'enews.imbc.com': ['iMBC News', imbcnews.from_imbcnews],
            'mbc.co.kr': ['MBC', 'kr', mbc.from_mbc],
            'newsjamm.co.kr': ['News Jamm', newsjamm.from_newsjamm],
            'osen.mt.co.kr': ['OSEN', osen.from_osen],
            'programs.sbs.co.kr': ['SBS Program', sbs.from_sbs],
            'ent.sbs.co.kr': ['SBS News', sbsnews.from_sbsnews],
            'post.naver.com': ['Naver Post', naverpost.from_naverpost],
            'news.naver.com': ['Naver News', navernews.from_navernews],
            'news1.kr': ['News1', news1.from_news1],
            'tvreport.co.kr': ['TV Report', tvreport.from_tvreport],
            'k-odyssey.com': ['K-odyssey', kodyssey.from_kodyssey],
            'tv.jtbc.co.kr': ['JTBC TV', tvjtbc.from_tvjtbc],
            'newsen.com': ['Newsen', newsen.from_newsen],
            'dazedkorea.com': ['Dazed Korea', dazedkorea.from_dazedkorea],
            'cosmopolitan.co.kr': ['Cosmopolitan', cosmopolitan.from_cosmopolitan],
            'marieclairekorea.com': ['Marie Claire Korea', marieclairekorea.from_marieclairekorea],
            'lofficielkorea.com': ["L'officiel Korea", lofficielkorea.from_lofficielkorea],
            'harpersbazaar.co.kr': ["Harper's Bazaar Korea", harpersbazaar.from_harpersbazaar],
            'wkorea.com': ['W Korea', wkorea.from_wkorea],
            'elle.co.kr': ['Elle Korea', elle.from_elle],
            'vogue.co.kr': ['Vogue Korea', vogue.from_vogue]
        }],
        # JAPANESE SITES
        'JP': [{
            'natalie.mu': ['Natalie 音楽ナタリー', 'jp', nataliemu.from_nataliemu],
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
                if site in url:
                    print("\n\033[1;31mSite name '%s'\033[0;0m" % site)
                    print("\033[1;30;43mUrl: %s\033[0;0m" % url)
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
                    except IndexError:
                        print("No pictures found")
                    except KeyboardInterrupt:
                        print("\r", end="")
                        print("KeyboardInterrupt detected. Exiting gracefully.")
                        sys.exit(0)
    elif args.a or args.url:
        try:
            check_site(args.url)
        except AttributeError:
            print("Usage: krsite-dl [OPTIONS] URL [URL...]\n")
            print("You must provide at least one URL.")
            print("Type 'krsite-dl -h' for more information.")
        except IndexError:
            print("No pictures found")
        except KeyboardInterrupt:
            print("\r", end="")
            print("KeyboardInterrupt detected. Exiting gracefully.")
            sys.exit(0)

if __name__ == '__main__':
    main()