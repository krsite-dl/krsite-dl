import os
from down.download import download_handler
import krsite_dl as kr

def dir_handler(img_list, title = None, date = None):
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
    if title != None and date != None and writer != None:
        dirs = kr.args.destination + '/' + writer + '/' + date[2:] + ' ' + title
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = kr.args.destination
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    download_handler(img_list, dirs)