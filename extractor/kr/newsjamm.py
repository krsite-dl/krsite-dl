import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="newsjamm.co.kr", name="Newsjamm")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('span', class_='PostContent_statusItem__AgJEE').text.strip()
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d')
    post_date_short = post_date.strftime('%y%m%d')

    content = soup.find('div', class_='PostContent_contentSection__ChFQz')

    img_list = []

    for item in content.findAll('img'):
        img_list.append(item.get('src'))

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