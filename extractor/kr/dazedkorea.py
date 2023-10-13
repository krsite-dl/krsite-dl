import requests
import datetime

from bs4 import BeautifulSoup

def from_dazedkorea(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('h1', class_='title').text.strip()
    post_summary = soup.find('h2', class_='summary').text.strip()
    post_title = post_title + ' ' + post_summary
    post_date = soup.find('time', class_='timestamp').text.strip()
    post_date_short = post_date.replace('/', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y/%m/%d')
    content = soup.find('div', class_='article-body')

    img_list = []
    
    for item in content.findAll('img'):
        img_list.append('http://dazedkorea.com' + item.get('src'))

    print("Title: %s" % post_title)
    print("Summary: %s" % post_summary)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)