import os
import re
import platform
from down.download import download_handler, download_handler_naver, download_handler_alt, download_handler_news1
import krsite_dl as kr

# windows reserved characters
reserved_pattern = r'[\\/:*?"<>|]'

# directory handling for press sites / blogs that have distinct topics
def dir_handler(img_list, title = None, post_date_short = None, post_date = None, loc = None, folder_name = None):
    if not kr.args.ai:
        if not kr.args.no_windows_filenames:
            title = re.sub(reserved_pattern, '', title)
    
    if title != None and post_date_short != None:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name, post_date_short + ' ' + title)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    if kr.args.ai:
        download_handler_alt(img_list, dirs, post_date, loc)
    else:
        download_handler(img_list, dirs, post_date, loc)


# directory handling for press sites / blogs that don't have distinct topics (e.g. news / random topics)
def dir_handler_alt(img_list, title = None, post_date_short = None, post_date = None, loc = None, folder_name = None):
    if not kr.args.no_windows_filenames:
        title = re.sub(reserved_pattern, '', title)

    if title != None and post_date_short != None:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name, post_date_short, title)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, dirs, post_date, loc)

# directory handling for news1 (news1.kr). Create a single directory, instead of multiple directories for each article we use the name of the article as image name
def dir_handler_news1(img_list, title = None, post_date_short = None, post_date = None, loc = None, folder_name = None):
    if not kr.args.no_windows_filenames:
        title = re.sub(reserved_pattern, '', title)

    if title != None and post_date_short != None:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler_news1(img_list, dirs, post_date, post_date_short, title, loc)

# directory handling for naver blogs
def dir_handler_naver(img_list, title = None, post_date_short = None, series = None, post_date = None, post_writer = None, folder_name = None):
    if not kr.args.no_windows_filenames:
        title = re.sub(reserved_pattern, '', title)
        post_writer = re.sub(reserved_pattern, '', post_writer)

    if title != None and post_date_short != None and series != None:
        dirs = os.path.join(kr.args.destination, 'krsite-dl', folder_name, post_writer, series, post_date_short + ' ' + title)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = os.path.jon(kr.args.destination, 'krsite-dl')
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler_naver(img_list, dirs, post_date)