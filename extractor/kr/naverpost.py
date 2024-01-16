"""Extractor for https://post.naver.com"""

import datetime
import time
import re
import json
import html

from rich import print
from selenium.common.exceptions import NoSuchElementException

from common.common_modules import SeleniumParser, SiteRequests
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="post.naver.com", name="Naver Post")


def get_data(hd):
    """Get data"""
    BASE = r"(?:https?://)?(?:m\.)?(post\.naver\.com)"
    pattern = BASE + r"(/my.)?(?:naver|nhn)"
    pattern2 = BASE + r"(/search/authorPost.)?(?:naver|nhn)"
    pattern3 = BASE + r"(/series.)?(?:naver|nhn)"
    pattern4 = BASE + r"(/my/series/detail.)?(?:naver|nhn)"
    pattern5 = BASE + r"(/viewer/postView.)?(?:naver|nhn)"

    def naverpost_search(hd):
        """Get data from search result"""
        parser = SeleniumParser()
        w = parser._requests(hd)

        post_list = set()

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'link_end'):
                    post_list.add(i.get_attribute('href'))

        w.quit()
        print(f"Found {len(post_list)} post(s)")

        for i in post_list:
            naverpost_post(i)

    def naverpost_series(hd):
        """Get data from series page"""
        parser = SeleniumParser()
        w = parser._requests(hd)

        series_list = set()

        sender_name = w.find_element(parser.get_by('CLASS_NAME'), 'name').text
        print("Sender: %s" % sender_name)

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'link'):
                    series_list.add(i.get_attribute('href'))

        w.quit()
        print(f"Found {len(series_list)} series")
        print("------------------\n")

        for i in series_list:
            naverpost_list(i)

    def naverpost_list(hd):
        """Get data from series list"""
        parser = SeleniumParser()
        w = parser._requests(hd)

        post_list = set()

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False
                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'spot_post_area'):
                    post_list.add(i.get_attribute('href'))

        w.quit()
        print(f"Found {post_list} post(s)")

        for i in post_list:
            naverpost_post(i)

    def naverpost_post(hd):
        """Get post data"""
        site_requests = SiteRequests()
        site = site_requests.session.get(hd).text

        post_writer = html.unescape(site.split("meta property=\"og:author\" content=\"")[1].split("\"")[0])
        post_series = html.unescape(re.sub(r'<i[^>]*>.*?</i>', '', site.split('<div class="se_series">')[1].split('</div>')[0]).strip())
        post_title = html.unescape(site.split("meta property=\"og:title\" content=\"")[1].split("\"")[0])
        post_date = site.split("meta property=\"og:createdate\" content=\"")[1].split("\"")[0]
        post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d. %H:%M:%S')
        post_date_short = post_date.strftime('%y%m%d')

        img_list = []
        for item in site.split("data-linkdata=\'")[1:]:
            linkdata = json.loads(item.split("\'>\n")[0])
            if 'storep' not in linkdata['src']:
                src = linkdata['src'].split('?')[0]
                img_list.append(src)


        print(f"\nWriter: {post_writer}")
        print(f"\nSeries: {post_series}")
        print(f"Title: {post_title}")
        print(f"Date: {post_date}")
        print(f"Found {len(img_list)} image(s)")

        dir = [SITE_INFO.name, post_writer, post_series,
               f"{post_date_short} {post_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option='naverpost',
        )

        DirectoryHandler().handle_directory(payload)

    if re.search(pattern, hd):
        print("[bold green]Naver Post Main Page[/bold green]")
        naverpost_search(hd)

    elif re.search(pattern2, hd):
        print("[bold green]Naver Post Search Result[/bold green]")
        naverpost_search(hd)

    elif re.search(pattern3, hd):
        print("[bold green]Naver Post Series Page[/bold green]")
        naverpost_series(hd)

    elif re.search(pattern4, hd):
        print("[bold green]Naver Post Series List[/bold green]")
        naverpost_list(hd)

    elif re.search(pattern5, hd):
        print("[bold green]Naver Post Page[/bold green]")
        naverpost_post(hd)
