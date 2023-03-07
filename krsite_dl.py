import argparse
import sys
import sites.dispatch as dispatch
import sites.imbcnews as imbcnews
import sites.newsjamm as newsjamm
import sites.osen as osen
import sites.sbs as sbs
import sites.mbc as mbc
import sites.naverpost as naverpost
import sites.generic as generic     

parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='?',type=str, help="valid news/blog url")
parser.add_argument("-a", type=str, help="text file containing site urls")
parser.add_argument("-ai", type=str, help="text file containing image urls")
parser.add_argument("--windows-filenames", action="store_true", help="Remove windows reserved characters from the title (enabled by default in Windows)")
# parser.add_argument("--board-no", type=int, help="The board number from a site (SBS). For example (https://programs.sbs.co.kr/enter/gayo/visualboard/54795?cmd=view&page=1&board_no=438994) will have a board no of 438994")
parser.add_argument("-d", "--destination", type=str, default=".",help="The destination path for the downloaded file")
args = parser.parse_args()


def check_site(url):
    url = url.strip()
    
    if 'dispatch.co.kr' in url:
        print("Site name 'Dispatch'")
        dispatch.from_dispatch(url)
        return
    if 'enews.imbc.com' in url:
        print("Site name 'iMBC News'")
        imbcnews.from_imbcnews(url)
        return
    if 'newsjamm.co.kr' in url:
        print("Site name 'News Jamm'")
        newsjamm.from_newsjamm(url)
        return
    if 'osen.mt.co.kr' in url:
        print("Site name 'OSEN'")
        osen.from_osen(url)
        return
    if 'sbs.co.kr' in url:
        print("Site name 'SBS'")
        sbs.from_sbs(url)
        return
    if 'mbc.co.kr' in url:
        print("Site name 'MBC와 함께'")
        mbc.from_mbc(url)
        return
    if 'post.naver.com' in url:
        print("Site name 'Naver 포스트'")
        naverpost.from_naverpost(url)
        return
    else:
        # print("URL invalid / Site not supported. [%s]" % url)
        print("Generic Sites %s *may not work" % url.split('/')[2])
        generic.from_generic(url)
        return


def main():
    if args.a:
        try:
            with open(args.a, 'r') as f:
                for line in f:
                    if line[0] == '#' or line[0] == ';' or line[0] == ']':
                        continue
                    elif line != '\n':
                        check_site(line)
        except FileNotFoundError:
            print("File not found: %s" % args.a)
    else:
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