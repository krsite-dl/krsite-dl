"""Extractor for https://blog.naver.com"""

import datetime
import re
import json
import html

from common.common_modules import Requests, Encode
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="blog.naver.com", name="Naver Blog")

def get_data(hd):
    """Get data"""
    BASE = r"(?:https?://)?(?:m\.)?(blog\.naver\.com)"
    pattern = BASE + r"(/PostView.)?(?:naver|nhn)\?blogId=(\w+)&logNo=(\d+)"
    pattern_al = pattern + r"(\w+)/(\d+)/?$)"
    pattern1 = BASE + r"(/PostList.)?(?:naver|nhn)\?blogId=(\w+)&(?:from=(\w+)&)?(categoryNo=(\d+))"
    pattern2 = BASE + r"(\w+)/(\d+)"
    # pattern3 = BASE + r"(/PostList.)?(?:naver|nhn)\?blogId=(\w+)&categoryNo=(\d+)&from=postList"

    root = "https://blog.naver.com"

    def naverblog_blog(hd):
        pass

    def naverblog_series(hd):
        """Get series"""
        #https://blog.naver.com/PostList.naver?blogId=jypentertainment&widgetTypeCall=true&topReferer=https%3A%2F%2Fblog.naver.com%2FPostList.naver%3FblogId%3Djypentertainment%26categoryNo%3D9%26from%3DpostList&trackingCode=blog_etc&directAccess=true#
        
        blog_id = hd.split('blogId=')[1].split('&')[0]
        category_no = hd.split('categoryNo=')[1].split('&')[0]

        # list_url = "{}/PostList.(?:naver|nhn)?blogId=(\w+)&categoryNo=(\d+)"
        # list_url = "{}/PostList.naver?blogId={}&categoryNo={}".format(root, blog_id, category_no)
        # print(list_url)



        #https://blog.naver.com/PostTitleListAsync.naver?blogId=starship_ent&viewdate=&currentPage=1&categoryNo=29&parentCategoryNo=&countPerPage=5
        series_url = "{}/PostTitleListAsync.naver".format(root)
        params = {
            'blogId': blog_id,
            'viewdate': '',
            'currentPage': 1,
            'categoryNo': category_no,
            'parentCategoryNo': '',
            'countPerPage': '5'
        }

        site_req = Requests()

        url_list = []
        while True:
            series = site_req.session.get(series_url, params=params).text.replace('\\', '')

            json_data = json.loads(series)

            for post in json_data['postList']:
                log_no = post['logNo']

                post_url = "{}/PostView.naver?blogId={}&logNo={}".format(root, blog_id, log_no)
                url_list.append(post_url)

            
            if (int(params['countPerPage']) * int(params['currentPage'])) >= int(json_data['totalCount']):
                site_req.session.close()
                break
            params['currentPage'] += 1

        print(f"Found {len(url_list)} post(s)")

        for i in url_list:
            naverblog_post(i)
        

    #https://blog.naver.com/PostList.naver?blogId=jypentertainment&categoryNo=9&from=postList
    #https://blog.naver.com/PostView.naver?blogId=jypentertainment&logNo=223719801689&categoryNo=0&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=&from=section
    #https://blog.naver.com/jypentertainment/223719801689

    """
    No matter the urls are, the final url (which is used to extract the data) will always be the same.
    1. https://blog.naver.com/PostView.naver?blogId=jypentertainment&logNo=223719801689&categoryNo=0&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=&from=section (something like this)

    So in that case we can just use the regex to extract the blogId and logNo fromt he url and then craft the final url.
    """

    def naverblog_post(hd):
        p = re.search(r'(?:https?://)?(?:m\.)?(blog\.naver\.com)/(\w+)/(\d+)', hd)
        if p:
            blog_id = p.group(2)
            post_id = p.group(3)
        else:
            p = re.search(r'(?:https?://)?(?:m\.)?(blog\.naver\.com)/PostView.(?:naver|nhn)\?blogId=(\w+)&logNo=(\d+)', hd)
            blog_id = p.group(2)
            post_id = p.group(3)

        post_url = "{}/PostView.naver?blogId={}&logNo={}".format(root, blog_id, post_id)

        site_req = Requests()
        site = site_req.session.get(post_url).text

        site = html.unescape(site).replace('\n', '').replace('\t', '').replace('\\', '')
        
        post_writer = html.unescape(site.split(
            "meta property=\"naverblog:nickname\" content=\"")[1]
            .split("\"")[0]).strip()
        post_series = html.unescape(re.sub(
                r'<a[^>]*>(.*?)</a>', lambda match: match.group(1), site.split(
                    '<div class="blog2_series">')[1]
                .split('</div>')[0]).strip())
        post_title = html.unescape(site.split(
            "meta property=\"og:title\" content=\"")[1].split("\"")[0].strip())
        post_date = html.unescape(re.search(
            r'<span class="[^"]*se_publishDate[^"]*">(.*?)</span>', site).group(1).strip())
        post_date = datetime.datetime.strptime(post_date, '%Y. %m. %d. %H:%M')
        post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        # Seems to be the only attribute
        pattern = re.compile(r"data-linkdata='([^']+)'")
        matches = pattern.finditer(site)
        index = '001'
        for match in matches:
            try:
                linkdata = json.loads(match.group(1))
                if 'src' in linkdata and 'storep' not in linkdata['src']:
                    src = str(linkdata['src'].split('?')[0].strip('\'"')).replace('postfiles', 'blogfiles')
                    if re.search(r'%[1-9A-Z]',src) is None:
                        img_list.append((src, index))
                        index = str(int(index) + 1).zfill(3)
                        continue

                    img_list.append(src)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

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
            option='naverblog',
            custom_headers={'Referer': root}
        )

        DirectoryHandler().handle_directory(payload)


    if (re.search(pattern1, hd)):
        print("Naver Blog Series")
        naverblog_series(hd)
    elif (re.search(pattern, hd)):
        print("Naver Blog Post")
        naverblog_post(hd)