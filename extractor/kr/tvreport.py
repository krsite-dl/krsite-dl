import requests
import datetime
import re

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="tvreport.co.kr", name="TV Report", location="KR")

def get_data(hd):
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

    DirectoryHandler().handle_directory_alternate(payload)