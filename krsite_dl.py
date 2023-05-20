import argparse
import sys
import extractor.dispatch as dispatch
import extractor.imbcnews as imbcnews
import extractor.newsjamm as newsjamm
import extractor.osen as osen
import extractor.sbs as sbs
import extractor.sbsnews as sbsnews
import extractor.mbc as mbc
import extractor.naverpost as naverpost
import extractor.navernews as navernews
import extractor.tvreport as tvreport
import extractor.kodyssey as kodyssey
import extractor.tvjtbc as tvjtbc
import extractor.dazedkorea as dazedkorea
import extractor.cosmopolitan as cosmopolitan
import extractor.marieclairekorea as marieclairekorea
import extractor.lofficielkorea as lofficielkorea
import extractor.generic as generic
import extractor.direct as direct

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='?',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
parser.add_argument("-ai", type=str, help="text file containing image urls")
parser.add_argument("--no-windows-filenames", action="store_true", help="By default krsite-dl will remove characters that are not allowed in Windows filenames. This option will disable that.")
# parser.add_argument("--force-date", type=str, help="Force a date for the downloaded file. Format: YYYYMMDD HHMMSS")
# parser.add_argument("--board-no", type=int, help="The board number from a site (SBS). For example (https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no=438994) will have a board no of 438994")
parser.add_argument("-d", "--destination", type=str, default=".",help="The destination path for the downloaded file")
args = parser.parse_args()


def check_site(url):
    site_dict = {
        'dispatch.co.kr': ['Dispatch', dispatch.from_dispatch],
        'enews.imbc.com': ['iMBC News', imbcnews.from_imbcnews],
        'mbc.co.kr': ['MBC', mbc.from_mbc],
        'newsjamm.co.kr': ['News Jamm', newsjamm.from_newsjamm],
        'osen.mt.co.kr': ['OSEN', osen.from_osen],
        'programs.sbs.co.kr': ['SBS Program', sbs.from_sbs],
        'ent.sbs.co.kr': ['SBS News', sbsnews.from_sbsnews],
        'post.naver.com': ['Naver Post', naverpost.from_naverpost],
        'news.naver.com': ['Naver News', navernews.from_navernews],
        'tvreport.co.kr': ['TV Report', tvreport.from_tvreport],
        'k-odyssey.com': ['K-odyssey', kodyssey.from_kodyssey],
        'tv.jtbc.co.kr': ['JTBC TV', tvjtbc.from_tvjtbc],
        'dazedkorea.com': ['Dazed Korea', dazedkorea.from_dazedkorea],
        'cosmopolitan.co.kr': ['Cosmopolitan', cosmopolitan.from_cosmopolitan],
        'marieclairekorea.com': ['Marie Claire Korea', marieclairekorea.from_marieclairekorea],
        'lofficielkorea.com': ["L'officiel Korea", lofficielkorea.from_lofficielkorea],
        'generic': ['Generic', generic.from_generic]
    }

    for site in site_dict:
        if site in url:
            print("\n\033[1;31mSite name '%s'\033[0;0m" % site_dict[site][0])
            print("\033[1;30;43mUrl: %s\033[0;0m" % url)
            site_dict[site][1](url)
            return
    else:
        print("\n\033[1;31mSite name '%s'\033[0;0m" % site_dict['generic'][0])
        print("\030[1;30;43mUrl: %s\033[0;0m" % url)
        site_dict['generic'][1](url)
        return
    

def main():
    try:
        if args.a:
            with open(args.a, 'r') as f:
                for line in f:
                    if line[0] == '#' or line[0] == ';' or line[0] == ']':
                        continue
                    elif line != '\n':
                        check_site(line)                        
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
    if not args.a or not args.ai:
        try:
            check_site(args.url)
        # except AttributeError:
        #     print("Usage: krsite-dl [OPTIONS] URL [URL...]\n")
        #     print("You must provide at least one URL.")
        #     print("Type 'krsite-dl -h' for more information.")
        except IndexError:
            print("No pictures found")
        except KeyboardInterrupt:
            print("\r", end="")
            print("KeyboardInterrupt detected. Exiting gracefully.")
            sys.exit(0)

if __name__ == '__main__':
    main()