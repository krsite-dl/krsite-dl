import requests
import datetime
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def from_mbc(hd, loc, folder_name):
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
        
        from down.directory import DirectoryHandler

        DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)


    mbc_post(hd)
