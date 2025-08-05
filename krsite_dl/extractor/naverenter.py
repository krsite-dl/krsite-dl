"""Extractor for https://entertain.naver.com"""

from ..utils.core import (
    Requests, 
    Logger, 
    Site,
    DataPayload,
    re,
    json,
    html,
    datetime, 
    )

SITE_INFO = Site(hostname="entertain.naver.com", name="Naver Entertain")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_req = Requests()

    site = site_req.session.get(hd).text

    post_title = site.split("<title>")[1].split("</title>")[0].strip()
    post_date = site.split('<em class="date">')[1].split("</em>")[0].strip()

    img_list = []
    site_req.session.close()
    logger.log_extractor_info(
        post_title, 
        post_date, 
        img_list
    )
