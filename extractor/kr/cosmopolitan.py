import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="cosmopolitan.co.kr", name="Cosmopolitan")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    post_title  = soup.find('h2', class_='tit_article').text.strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S')
    content = soup.find('div', class_='atc_content')

    img_list = []
    
    for item in content.findAll('img'):
        img_list.append(item.get('src'))

    head_img = soup.find('div', class_='article_head')
    
    if head_img.get('style') is not None:
        img_list.append(head_img['style'].split('url(')[1].split(')')[0].replace('"',''))

    print("Title: %s" % post_title)
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