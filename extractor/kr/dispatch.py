import requests
import re
import datetime
from bs4 import BeautifulSoup
import down.directory as dir
def from_dispatch(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []
    post_date = soup.find('div', class_='post-date').text.strip()
    post_title = soup.find('div', class_='page-post-title').string.strip()
    post_date_short = post_date.replace('.', '')[2:8]

    for i in soup.findAll('img', class_='post-image'):
        if i.get('data-src') != None:
            temp = i.get('data-src')
            img_list.append(temp)
        else:
            temp = i.get('src')
            img_list.append(temp)

    post_date = post_date[:19].replace('.', '')
    if '오전' in post_date:
        post_date = datetime.datetime.strptime(post_date.replace('오전', 'AM'), '%Y%m%d %p %I:%M')
    elif '오후' in post_date:
        post_date = datetime.datetime.strptime(post_date.replace('오후', 'PM'), '%Y%m%d %p %I:%M')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))
    
    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date, loc, folder_name)