import requests
import datetime
import re

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup

def from_tvreport(hd, loc, folder_name):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
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

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory_alternate(img_list, post_title, post_date, post_date_short, loc, folder_name)