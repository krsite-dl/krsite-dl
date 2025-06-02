"""Extractor for https://spur.hpplus.jp"""

from ..utils.core import (
    Requests,  
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="spur.hpplus.jp", name="Spurjp")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_req = Requests()
    site = site_req.session.get(hd).text
    
    post_title = re.search(r'<div class="article-header-inner">.*?<h1>(.*?)</h1>', site, re.DOTALL).group(1).strip()
    post_date = re.search(r'<div class="article-header-inner">.*?<div class="flex">.*?<div class="posted-date">(.*?)</div>', site, re.DOTALL).group(1).strip()
    post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d')
    post_date_short = post_date.strftime('%Y%m%d')[2:]
    
    
    img_list = []
    # grab everything from wysiwyg
    for content in re.finditer(r'<div class="wysiwyg">.*?</div>', site, re.DOTALL):
        content = content.group()
        for img in re.finditer(r'<img.*?src="(.*?)"', content):
            img_list.append(img.group(1))

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
        custom_headers={'Referer': 'https://spur.hpplus.jp'}
    )

    yield payload
