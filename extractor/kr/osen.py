import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname=["osen.mt.co.kr", "osen.co.kr"], name="OSEN", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    wrap = soup.find('div', class_='detailTitle')

    post_title = wrap.find('h1').text
    post_date = soup.find('div', class_='detailTitle__post-infos').text.strip()

    img_list = []

    for item in soup.findAll('img', class_='view_photo'):
        img_list.append('https:' + item['src'].split(':')[1])

    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    post_date_short = post_date.strftime('%Y%m%d')[2:]

    print("Post title: %s" % post_title)
    print("Post date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))
    
    dir = [SITE_INFO.name, post_date_short]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option='combine',
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)