import datetime
import re

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="tvreport.co.kr", name="TV Report", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)
    
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

    dir = [SITE_INFO.name, post_date_short, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)