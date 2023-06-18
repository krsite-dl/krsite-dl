import datetime
from pytz import timezone
import json
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs, unquote
import down.directory as dir

def from_lofficielsingapore(hd, loc, folder_name):
    img_list = []

    opt = Options()
    opt.add_argument('--headless')
    w = wd.Chrome(options=opt)

    w.get(hd)

    wait = WebDriverWait(w, 10)

    article_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.article-layout__main')))
    image_elements = article_element.find_elements(By.TAG_NAME, 'img')

    for image_element in image_elements:
        wait.until(EC.visibility_of(image_element))
        w.execute_script("arguments[0].scrollIntoView();", image_element)

        srcset_value = image_element.get_attribute('src')
        try:
            url = parse_qs(urlparse(srcset_value).query)['url'][0].split('?')[0]
            img_list.append(url)
        except KeyError:
            continue

    script_tag = w.find_element(By.XPATH, '//script[@type="application/ld+json"]')
    json_data = json.loads(script_tag.get_attribute('textContent'))

    post_title = json_data['headline']
    post_date = json_data['datePublished']
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    tz = timezone('Asia/Singapore')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    w.quit()

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))
    
    dir.dir_handler(img_list, post_title, post_date_short, post_date, loc, folder_name)