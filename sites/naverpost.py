import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from down.directory import dir_handler_naver

def from_naverpost(hd):
    def naverpost_topic(hd):
        opt = Options()
        opt.add_argument('--headless')
        w = wd.Chrome(options=opt)
        w.get(hd)
        
        post_list = set()

        btn = w.find_element(By.CLASS_NAME, '_more')

        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False
                for i in w.find_elements(By.CLASS_NAME, 'spot_post_area'):
                    post_list.add('https://post.naver.com' + i.get_attribute('href'))

        w.quit()

        print("Found %s post(s)" % len(post_list))
        
        for i in post_list:
            naverpost_post(i)


    def naverpost_post(hd):
        opt = Options()
        opt.add_argument('--headless')
        w = wd.Chrome(options=opt)
        w.get(hd)

        
        try:
            post_writer = w.find_element(By.CLASS_NAME, 'se_author').text
            post_title = w.find_element(By.CLASS_NAME, 'se_textarea').text.replace('\n', ' ')
            post_date = w.find_element(By.CLASS_NAME, 'se_publishDate').text.replace('.', '')[:8]
        except Exception:
            post_writer = w.find_element(By.CLASS_NAME, 'writer').text
            post_title = w.find_element(By.CLASS_NAME, 'title').text.replace('\n', ' ')
            post_date = w.find_element(By.CLASS_NAME, 'post_date').text.replace('.', '')[:8]


        special_chars = r'\/:*?"<>|'

        for i in special_chars:
            post_title = post_title.replace(i, '')

        img_list = []

        print("Writer: %s" % post_writer)
        print("Title: %s" % post_title)
        print("Date: %s" % post_date)

        for i in w.find_elements(By.CLASS_NAME, 'se_mediaImage'):
            img_list.append(str(i.get_attribute('src').split('?')[0]))

        for i in w.find_elements(By.CLASS_NAME, 'img_attachedfile'):
            img_list.append(str(i.get_attribute('src').split('?')[0]))

        w.quit()

        print("Found %s image(s)" % len(img_list))

        dir_handler_naver(img_list, post_title, post_date, post_writer)


    if 'my.naver' in hd:
        print("Post Dashboard")
        # naverpost_agency(hd)
    elif 'detail.naver' in hd:
        print("Post Topic")
        naverpost_topic(hd)
    elif 'postView.naver' in hd:
        print("Post")
        naverpost_post(hd)