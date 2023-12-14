import datetime
import json

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="lofficielsingapore.com", name="L'Officiel Singapore", location="SG")

def get_data(hd):
    img_list = []

    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    next_data = soup.find('script', id='__NEXT_DATA__').contents[0]

    json_data = json.loads(next_data)

    post_infos = json_data['props']['pageProps']['subscription']['initialData']['article']

    post_title = post_infos['title']
    post_date = post_infos['_publishedAt']
    post_date_short = post_date.replace('-', '')[2:8]
    # 2022-09-21T16:13:39+09:00
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    post_date = post_date.replace(tzinfo=None)

    # get post cover
    img_list.append(post_infos['postCover'][0]['coverImage']['url'].split('?')[0])
    post_blocks = post_infos['postBlocks']
    for post_block in post_blocks:
        if post_block['__typename'] == 'ImageBoxRecord':
            img_list.append(post_block['image']['url'].split('?')[0])

        if post_block['__typename'] == 'AdaptiveGalleryRecord':
            for image in post_block['images']:
                img_list.append(image['url'].split('?')[0])

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

    DirectoryHandler().handle_directory(payload)