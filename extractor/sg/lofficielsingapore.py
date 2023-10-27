import datetime
import json
import re

from common.data_structure import Site, ScrapperPayload
from pytz import timezone
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs, unquote

SITE_INFO = Site(hostname="lofficielsingapore.com", name="L'Officiel Singapore", location="SG")

def get_data(hd):
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
    post_title = re.sub(r'&amp;|quot;', '', post_title)
    post_date = json_data['datePublished']
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    tz = timezone('Asia/Singapore')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    w.quit()

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
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