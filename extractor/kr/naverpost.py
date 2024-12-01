"""Extractor for https://post.naver.com"""

import datetime
import re
import json
import html

from rich import print

from common.common_modules import Requests, Encode
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

    encode = Encode()

    def naverpost_main(hd):
        """Get data from main page"""
        member_no = hd.split('memberNo=')[1].split('&')[0]

        main_api = 'https://post.naver.com/async/my.naver'
        params = {
            'memberNo': member_no,
            'postListViewType': 0,
            'isExpertMy': 'true',
            'fromNo': 1,
            'totalCount': 0,
        }

        site_req = Requests()

        post = set()

        while True:
            req = site_req.session.get(
                main_api, params=params).text

            nfn_val = req.split('"nextFromNo":')[1].split(',')[0].strip('"')
            html_cont = req.split('"html":"')[1].split('","')[0]
            html_cont = html.unescape(html_cont)
            html_cont = html_cont.replace('\\n', '').replace(
                '\\t', '').replace('\\', '')

            for i in html_cont.split('<a href="')[1:]:
                p = i.split('"')[0]
                if 'commentsView.naver' not in p and '#' not in p:
                    post.add("https://post.naver.com" + p)

            params['fromNo'] = nfn_val

            if nfn_val == "":
                break

        site_req.session.close()
        print(f"Found {len(post)} post(s)")

        for i in post:
            naverpost_post(i)

    def naverpost_search(hd):
        """Get data from search result"""
        keyword = hd.split('keyword=')[1].split('&')[0]
        member_no = hd.split('memberNo=')[1].split('&')[0]

        keyword = encode._encode_kr(keyword)

        search_api = 'https://post.naver.com/search/authorPost/more.naver'
        params = {
            'keyword': keyword,
            'memberNo': member_no,
            'sortType': 'createDate.dsc',
            'fromNo': 1,
        }

        site_req = Requests()

        post = set()

        while True:
            req = site_req.session.get(search_api, params=params).text
            nfn_val = req.split('"nextFromNo":')[1].split(',')[0].strip('"')
            html_cont = req.split('"html":"')[1].split('","')[0]
            html_cont = html.unescape(html_cont)
            html_cont = html_cont.replace('\\n', '').replace(
                '\\t', '').replace('\\', '')

            for i in html_cont.split('<a href="')[1:]:
                p = re.sub(r'&searchRank=\d+', '', i.split('"')[0])
                if 'detail.naver' not in p and 'commentsView.naver' not in p and '#' not in p:
                    post.add("https://post.naver.com" + p)

            params['fromNo'] = nfn_val

            if nfn_val == "":
                break

        site_req.session.close()
        print(f"Found {len(post)} post(s)")

        for i in post:
            naverpost_post(i)

    def naverpost_series(hd):
        """Get data from series page"""
        member_no = hd.split('memberNo=')[1].split('&')[0]

        series_list_api = 'https://post.naver.com/async/series.naver'
        params = {
            'memberNo': member_no,
            'postListViewType': 0,
            'isExpertMy': 'true',
        }

        site_req = Requests()

        series = []

        while True:
            req = site_req.session.get(
                series_list_api, params=params).text

            nfn_val = req.split('"nextFromNo":')[1].split(',')[0].strip('"')
            html_cont = req.split('"html":"')[1].split('","')[0]
            html_cont = html.unescape(html_cont)
            html_cont = html_cont.replace('\\n', '').replace(
                '\\t', '').replace('\\', '')

            for i in html_cont.split('<a href="')[1:]:
                series.append("https://post.naver.com" + i.split('"')[0])

            params['fromNo'] = nfn_val

            if nfn_val == "":
                break

        site_req.session.close()
        print(f"Found {len(series)} series(s)")

        for i in series:
            naverpost_list(i)

    def naverpost_list(hd):
        """Get data from series list"""

        member_no = hd.split('memberNo=')[1].split('&')[0]
        series_no = hd.split('seriesNo=')[1].split('&')[0]

        post_list_api = 'https://post.naver.com/my/series/detail/more.nhn'
        params = {
            'memberNo': member_no,
            'seriesNo': series_no,
            'lastSortOrder': 1,
            'prevVolumeNo': '',
            'fromNo': 1,
            'totalCount': 0,
        }

        site_req = Requests()

        post = []

        while True:
            req = site_req.session.get(post_list_api, params=params).text
            nfn_val = req.split('"nextFromNo":')[1].split(',')[0].strip('"')
            html_cont = req.split('"html":"')[1].split('","')[0]
            html_cont = html.unescape(html_cont)
            html_cont = html_cont.replace('\\n', '').replace(
                '\\t', '').replace('\\', '')

            for i in html_cont.split('<a href="')[1:]:
                post.append("https://post.naver.com" + i.split('"')[0])

            params['fromNo'] = nfn_val

            if nfn_val == "":
                break

        site_req.session.close()
        print(f"Found {len(post)} post(s)")

        for i in post:
            naverpost_post(i)

    def naverpost_post(hd):
        """Get post data"""
        site_req = Requests()
        site = site_req.session.get(hd).text

        post_writer = html.unescape(site.split(
            "meta property=\"og:author\" content=\"")[1]
            .split("\"")[0]).strip()
        try:
            post_series = html.unescape(re.sub(
                r'<i[^>]*>.*?</i>', '', site.split(
                    '<div class="se_series">')[1]
                .split('</div>')[0]).strip())
        except IndexError:
            try:
                post_series = html.unescape(site.split(
                    'class="series ">')[1]
                    .split('</a>')[0].strip())
            except IndexError:
                print("Post series not found")
                post_series = ""
        post_series = re.sub(r'\s+', ' ', post_series)
        post_title = html.unescape(site.split(
            "meta property=\"og:title\" content=\"")[1].split("\"")[0].strip())
        post_title = re.sub(r'\s+', ' ', post_title)
        post_date = site.split("meta property=\"og:createdate\" content=\"")[
            1].split("\"")[0].strip()
        post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d. %H:%M:%S')
        post_date_short = post_date.strftime('%y%m%d')

        img_list = set()

        # [ IMAGE FROM DIFFERENT POST LAYOUT ]
        # Get Image from header
        pattern0 = re.compile(r'style="background-image: url\(([^)]+)\)')
        matches = pattern0.findall(site)
        for match in matches:
            src = match.split('?')[0].strip('\'"')
            img_list.add(src)

        # Get Image from new post layout
        pattern = re.compile(r"data-linkdata='([^']+)'")
        matches = pattern.findall(site)
        for match in matches:
            try:
                linkdata = json.loads(match)
                if 'src' in linkdata and 'storep' not in linkdata['src']:
                    src = linkdata['src'].split('?')[0].strip('\'"')
                    img_list.add(src)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        # Get Image from older post layout
        pattern2 = re.compile(r'data-realImagePath="([^"]+)"')
        matches2 = pattern2.findall(site)
        for match in matches2:
            if 'storep' not in match:
                src = match.split('?')[0].strip('\'"')
                img_list.add(src)

        site_req.session.close()
        print(f"Writer: {post_writer}")
        print(f"Series: {post_series}")
        print(f"Title: {post_title}")
        print(f"Date: {post_date}")
        print(f"Found {len(img_list)} image(s)")

        dir = [SITE_INFO.name, post_writer, post_series,
               f"{post_date_short} {post_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option='naverpost',
            custom_headers={'Referer': 'https://post.naver.com/'}
        )

        DirectoryHandler().handle_directory(payload)

    if re.search(pattern, hd):
        print("[bold green]Naver Post Main Page[/bold green]")
        naverpost_main(hd)

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
