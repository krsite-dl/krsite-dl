import requests
import re
import os
import krsite_dl as kr
import selenium.webdriver as wd
import selenium.webdriver.chrome.options as options

# windows reserved characters
reserved_pattern = r'[\\/:*?"<>|]'

def video_handler(video_list, title = None, post_date_short = None, post_date = None, loc = None, folder_name = None):
    if title != None and post_date_short != None:
        dirs = os.path.join(kr.args.destination, folder_name, post_date_short + ' ' + title)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
    else:
        dirs = os.path.join(kr.args.destination, folder_name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    for video in video_list:
        sel(video)


def sel(video):
    options = wd.ChromeOptions()
    options.add_argument('--headless')

    driver = wd.Chrome(options=options)
    
    driver.get(video)
    
    script = driver.find_element_by_tag_name('script')
    driver.close()

    print(script.get_attribute('innerHTML'))