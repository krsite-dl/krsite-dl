import datetime
import re

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="k-odyssey.com", name="K-odyssey")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    img_list = []

    post_title = soup.find('div', class_='viewTitle').find('h1').text.strip()
    post_date = soup.find('div', class_='dd').text.strip()
    post_date_short = re.sub('[\u3131-\uD7A3]+|\/|-|\s', '', post_date)[2:8]
    content = soup.find('div', class_='sliderkit-panels')

    for i in content.find_all('img'):
        img_list.append('https://k-odyssey.com' + i['src'].replace('_thum', ''))


    post_date = re.sub('[\u3131-\uD7A3]+|\/|-|\s+', '', post_date)
    post_date = post_date[:8] + ' ' + post_date[8:]
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %H:%M:%S')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date_short)
    print("Found %s image(s)" % len(img_list))

    dir = [SITE_INFO.name, post_date_short, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)