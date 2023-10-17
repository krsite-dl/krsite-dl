import requests
import datetime
import re

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup

def from_sbsnews(hd, loc, folder_name):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('h1', class_='cth_title').text.strip()
    post_date = soup.find('span', class_='cth_text').text
    post_date = re.sub('[\u3131-\uD7A3]+', '', post_date).strip()
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d %H:%M')
    content = soup.find('div', class_='w_ctma_text')
    post_date_short = post_date.strftime('%y%m%d')
    img_list = []

    for i in content.find_all('img'):
        img_list.append(i.get('data-v-src'))


    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory_alternate(img_list, post_title, post_date, post_date_short, loc, folder_name)