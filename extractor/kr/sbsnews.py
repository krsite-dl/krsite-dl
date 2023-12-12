import datetime
import re

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="ent.sbs.co.kr", name="SBS News", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


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