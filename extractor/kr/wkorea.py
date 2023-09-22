import requests
import re
import datetime
from pytz import timezone
from bs4 import BeautifulSoup
import down.video_handler as video_handler

def from_wkorea(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='post-content')

    img_list = set()
    for item in content.findAll('img'):
        i = item.get('src')
        img_list.add(i.split('-')[0] + '.' + i.split('.')[-1])

    # if the site contains any video

    video_list = []
    for video in content.findAll('iframe'):
        v = video.get('src')
        video_list.append(v)

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))
    if video_list:
        print("Found %s video(s)" % len(video_list))

        video_handler.video_handler(video_list, post_title, post_date_short, post_date, loc, folder_name)

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)