"""Extractor for https://newsen.com"""

from utils.core import (
    Requests, 
    Encode, 
    Logger, 
    Misc, 
    Site,
    DataPayload,
    re,
    json,
    html,
    datetime, 
    )

SITE_INFO = Site(hostname="newsen.com", name="Newsen")


def get_data(hd):
    """Get data"""
    print("Broken")
    # parser = SeleniumParser()
    # w = parser._requests(hd)

    # post_title = w.find_element(parser.get_by(
    #     'XPATH'), '//meta[@property="og:title"]').get_attribute('content').strip()
    # post_date = w.find_element(parser.get_by(
    #     'XPATH'), '//meta[@property="article:published_time"]').get_attribute('content').strip()
    # post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
    # post_date_short = post_date.strftime('%y%m%d')

    # content = w.find_element(parser.get_by('CLASS_NAME'), 'article')
    # img_elements = content.find_elements(parser.get_by('TAG_NAME'), 'img')

    # img_list = []

    # for img_element in img_elements:
    #     if not 'button' in img_element.get_attribute('src'):
    #         img_list.append(img_element.get_attribute(
    #             'src').replace('https', 'http'))

    # w.quit()

    # site_requests = Requests()

    # site = site_requests.session.get(hd).text

    # print(site)
    # site_req.session.close()
    # logger.log_extractor_info(
    #     post_title, 
    #     post_date, 
    #     img_list
    # )

    # dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]
    
    # payload = DataPayload(
    #     directory_format=dir,
    #     media=img_list,
    #     option=None,
    # )

    # yield payload
