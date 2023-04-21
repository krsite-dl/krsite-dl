import os
import re
import platform
from down.download import download_handler, download_handler_naver, download_handler_alt
import krsite_dl as kr

# windows reserved characters
reserved_pattern = r'[\\/:*?"<>|]'
def dir_handler(img_list, title = None, post_date_short = None, post_date = None):
    if not kr.args.ai:
        if not kr.args.no_windows_filenames:
            title = re.sub(reserved_pattern, '', title)
    
    if title != None and post_date_short != None:
        dirs = kr.args.destination + '/' + post_date_short + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    if kr.args.ai:
        download_handler_alt(img_list, dirs, post_date)
    else:
        download_handler(img_list, dirs, post_date)


def dir_handler_alt(img_list, title = None, post_date_short = None, post_date = None):
    if not kr.args.no_windows_filenames:
        title = re.sub(reserved_pattern, '', title)

    if title != None and post_date_short != None:
        dirs = kr.args.destination + '/' + post_date_short
        subdirs = dirs + '/' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            if not os.path.exists(dirs + '/' + title):               
                os.makedirs(subdirs)
        else:
            if not os.path.exists(dirs + '/' + title):
                os.makedirs(subdirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, subdirs, post_date)
    

def dir_handler_naver(img_list, title = None, post_date_short = None, series = None, post_date = None, post_writer = None):
    if not kr.args.no_windows_filenames:
        title = re.sub(reserved_pattern, '', title)

    if title != None and post_date_short != None and series != None:
        dirs = kr.args.destination + '/' + post_writer + '/' + series + '/' + post_date_short + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler_naver(img_list, dirs, post_date)