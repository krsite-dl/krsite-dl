import datetime
import re

from pytz import timezone
from urllib.parse import urlparse
from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="isplus.com", name="Ilgan Sports")

def get_data(hd):
    host = f"{urlparse(hd).scheme}://{urlparse(hd).netloc}"
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    post_title = soup.find('meta', property='og:title')['content']
    post_date = soup.find('meta', property='article:modified_time')['content']
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='article_body')

    img_list = []

    for img in content.findAll('img'):
        if img.get('src'):
            img = re.sub(re.compile(r'\.\d+x\.\d+'), '', img.get('src'))
            img_list.append(f"{host}{img}")

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