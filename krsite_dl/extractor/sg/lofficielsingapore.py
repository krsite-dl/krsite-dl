"""Extractor for https://lofficielsingapore.com"""""

from utils.core import (
    Requests,
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    json,
    datetime, 
    )

SITE_INFO = Site(hostname="lofficielsingapore.com", name="L'Officiel Singapore")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()
    soup = site_parser._parse(site_req.session.get(hd).text)
    next_data = soup.find('script', id='__NEXT_DATA__').contents[0]
    json_data = json.loads(next_data)
    post_infos = json_data['props']['pageProps']['subscription']['initialData']['article']
    post_title = post_infos['title']
    post_date = post_infos['_publishedAt']
    post_date_short = post_date.replace('-', '')[2:8]
    # 2022-09-21T16:13:39+09:00
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    post_date = post_date.replace(tzinfo=None)

    img_list = []
    # get post cover
    img_list.append(post_infos['postCover'][0]
                    ['coverImage']['url'].split('?')[0])
    post_blocks = post_infos['postBlocks']
    for post_block in post_blocks:
        if post_block['__typename'] == 'ImageBoxRecord':
            img_list.append(post_block['image']['url'].split('?')[0])

        if post_block['__typename'] == 'AdaptiveGalleryRecord':
            for image in post_block['images']:
                img_list.append(image['url'].split('?')[0])

    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )

    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]
    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
        custom_headers=None
    )

    yield payload
