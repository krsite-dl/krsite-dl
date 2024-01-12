import datetime

from pytz import timezone
from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="news1.kr", name="News1", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    post_title = soup.find('meta', property='og:title')['content'].strip().encode('latin-1').decode('utf-8', 'ignore')
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)
    post_date_short = post_date.strftime('%y%m%d')

    article = soup.find('div', id='article_body_content')

    img_list = []
    for item in article.findAll('img'):
        if 'kakao' not in item['src']:
            img_list.append((item['src'].replace('article', 'original'), item['alt'].strip()))
            # print(item['alt'].strip())

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir = [SITE_INFO.name, post_date_short]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option='combine',
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handler_directory(payload)