import requests
import datetime

from common.data_structure import Site, ScrapperPayload
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

SITE_INFO = Site(hostname="mbc.co.kr", name="MBC", location="KR")

def get_data(hd):
    opt = Options()
    opt.add_argument('--headless')
    w = wd.Chrome(options=opt)

    def mbc_post(hd):
        w.get(hd)

        post_title = w.find_element(By.TAG_NAME, 'h2').text
        post_date = w.find_element(By.CLASS_NAME, 'date').text
        post_date_short = post_date.replace('/', '')[2:8]
        post_date = datetime.datetime.strptime(post_date, '%Y/%m/%d (금) %H:%M')
        img_list = []

        print("Title: %s" % post_title)
        print("Date: %s" % post_date)

        for i in w.find_element(By.CLASS_NAME, 'img_down').find_elements(By.TAG_NAME, 'a'):
            img_list.append(i.get_attribute('href'))

        w.quit()

        print("Found %s image(s)" % len(img_list))
        
        payload = ScrapperPayload(
            title=post_title,
            shortDate=post_date_short,
            mediaDate=post_date,
            site=SITE_INFO.name,
            series=None,
            writer=None,
            location=SITE_INFO.location,
            media=img_list,
        )
        from down.directory import DirectoryHandler

        DirectoryHandler().handle_directory(payload)


    mbc_post(hd)
