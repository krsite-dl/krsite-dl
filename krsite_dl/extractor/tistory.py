"""Extractor for https://tistory.com/"""

from ..utils.core import (
    Requests, 
    Logger, 
    Site,
    DataPayload,
    re,
    html,
    datetime, 
    )

SITE_INFO = Site(hostname="tistory.com", name="Tistory", location="KR")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    site_req = Requests()
    site = site_req.session.get(hd).text

    post_article_author = html.unescape(site.split(
        "<meta property=\"og.article.author\" content=\"")[1].split("\"")[0].strip())
    post_title = html.unescape(site.split("<meta property=\"og:title\" content=\"")[
                               1].split("\"")[0].strip())
    post_date = html.unescape(site.split("<meta property=\"article:published_time\" content=\"")[
        1].split("\"")[0].strip())

    post_date = datetime.datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S%z")
    post_date_short = post_date.strftime('%y%m%d')

    # Normal article div pattern. (experimental) Might need further adjustment.
    # pattern = r'<div\s+[^>]*id=["\']article-view["\'][^>]*>(.*?)</div>'
    pattern = r'<div\s+[^>]*class=["\']tt_article_useless_p_margin[^"\']*["\'][^>]*>(.*?)</div>'

    article = re.search(pattern, site, re.DOTALL).group(1)

    img_list = []

    pattern = re.compile(r'<img\s[^>]*>')
    matches = pattern.findall(article)
    counter = 1
    for match in matches:
        img = match.split('src="')[1].split('"')[0]
        try:
            img_name = match.split('data-filename="')[1].split('"')[0]
        except IndexError:
            img_name = f'{counter}'
            counter += 1
        img_list.append((img, img_name))

    site_req.session.close()
    logger.log_extractor_info(
        f"Author: {post_article_author}",
        post_title,
        post_date,
        img_list
    )

    dir = [SITE_INFO.name, post_article_author,
           f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option='defined',
        custom_headers=None
    )

    yield payload
