import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="news.naver.com", name="Naver News")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    
    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('span', class_='_ARTICLE_DATE_TIME')['data-date-time'].strip()
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    post_date_short = post_date.strftime('%y%m%d')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    article = soup.find('div', class_='newsct_article')
    
    img_list = []
    for item in article.findAll('img'):
        # print(item)
        img_list.append(item.get('data-src').split('?')[0])

    print("Found %s image(s)" % len(img_list))

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)