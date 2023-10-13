import datetime

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def from_newsen(hd, loc, folder_name):
    opt = Options()
    opt.add_argument('--headless')
    w = wd.Chrome(options=opt)
    w.get(hd)

    post_title = w.find_element(By.XPATH, '//meta[@property="og:title"]').get_attribute('content').strip()
    post_date = w.find_element(By.XPATH, '//meta[@property="article:published_time"]').get_attribute('content').strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    content = w.find_element(By.CLASS_NAME, 'article')
    img_elements = content.find_elements(By.TAG_NAME, 'img')

    img_list = []

    for img_element in img_elements:
        if not 'button' in img_element.get_attribute('src'):
            img_list.append(img_element.get_attribute('src').replace('https', 'http'))

    w.quit()

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)
