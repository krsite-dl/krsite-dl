import requests
import re
import datetime
from bs4 import BeautifulSoup
import down.directory as dir

def from_tvreport(hd):
    r = requests.get(hd)

    soup = BeautifulSoup(r.text, 'html.parser')

    img_list = []

    post_title = soup.find('h1', class_='entry-title').text.strip()
    post_date = soup.find('time').text.strip()

    for i in soup.find_all('p', class_='dp-image-container'):
        img_list.append(i.find('img')['src'])


    post_date = re.sub('[\u3131-\uD7A3]+|\s+', '', post_date)
    post_date = post_date + ' ' + '00:00:00'
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)