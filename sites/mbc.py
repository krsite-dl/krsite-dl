import requests
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import down.directory as dir

def from_mbc(hd):
    opt = Options()
    opt.add_argument('--headless')
    w = wd.Chrome(options=opt)

    def mbc_post(hd):
        w.get(hd)

        post_title = w.find_element(By.TAG_NAME, 'h2').text
        post_date = w.find_element(By.CLASS_NAME, 'date').text.replace('/', '')[:8]

        img_list = []

        print("Title: %s" % post_title)
        print("Date: %s" % post_date)

        for i in w.find_element(By.CLASS_NAME, 'img_down').find_elements(By.TAG_NAME, 'a'):
            img_list.append(i.get_attribute('href'))

        w.quit()

        print("Found %s image(s)" % len(img_list))
        
        dir.dir_handler(img_list, post_title, post_date)


    mbc_post(hd)
