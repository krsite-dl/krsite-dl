import os
import re
import platform
from down.download import download_handler
import krsite_dl as kr

def dir_handler(img_list, title = None, date = None):
    if platform.system() == 'Windows':
        kr.args.windows_filenames = True

    if kr.args.windows_filenames:
        # windows reserved characters
        reserved_pattern = r'[\\/:*?"<>|]'
        title = re.sub(reserved_pattern, '', title)
    
    if title != None and date != None:
        dirs = kr.args.destination + '/' + date[2:] + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, dirs)


def dir_handler_alt(img_list, title = None, date = None):
    if platform.system() == 'Windows':
        kr.args.windows_filenames = True

    if kr.args.windows_filenames:
        # windows reserved characters
        reserved_pattern = r'[\\/:*?"<>|]'
        title = re.sub(reserved_pattern, '', title)

    if title != None and date != None:
        dirs = kr.args.destination + '/' + date[2:]
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

    download_handler(img_list, subdirs)
    

def dir_handler_naver(img_list, title = None, date = None, writer = None):
    if platform.system() == 'Windows':
        kr.args.windows_filenames = True

    if kr.args.windows_filenames:
        # windows reserved characters
        reserved_pattern = r'[\\/:*?"<>|]'
        title = re.sub(reserved_pattern, '', title)

    if title != None and date != None and writer != None:
        dirs = kr.args.destination + '/' + writer + '/' + date[2:] + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, dirs)