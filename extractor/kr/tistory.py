"""Extractor for https://tistory.com/"""

import datetime
import re
import html

from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="tistory.com", name="Tistory", location="KR")


def get_data(hd):
    site_parser = SiteParser()
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
    for match in matches:
        img = match.split('src="')[1].split('"')[0]
        img_name = match.split('data-filename="')[1].split('"')[0]
        img_list.append((img, img_name))

    site_req.session.close()
    print(f"Author: {post_article_author}")
    print(f"Title: {post_title}")
    print(f"Date: {post_date}")
    print(f"Found {len(img_list)} image(s)")

    dir = [SITE_INFO.name, post_article_author,
           f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option='defined',
    )

    DirectoryHandler().handle_directory(payload)
