import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="dazedkorea.com", name="Dazed Korea")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


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

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)