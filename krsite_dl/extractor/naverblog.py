"""Extractor for https://blog.naver.com"""

from ..utils.core import (
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

SITE_INFO = Site(hostname="blog.naver.com", name="Naver Blog")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    BASE = r"(?:https?://)?(?:m\.)?(blog\.naver\.com)"
    blog_pattern = BASE + r"(/\w+\/?$)"
    postview_pattern = BASE + r"(?:((/PostView.)?(?:naver|nhn)\?blogId=(\w+)&logNo=(\d+).*)|/(\w+)/(\d+)(?:\?.*)?$)"
    postlist_pattern = BASE + r"(/PostList.)?(?:naver|nhn)\?blogId=(\w+)&(?:from=(\w+)&)?(categoryNo=(\d+))"

    root = "https://blog.naver.com"
    root_m = "https://m.blog.naver.com"

    def naverblog_blog(hd):
        """Get entire blog"""
        blog_id = re.match(blog_pattern, hd).group(2).strip('/')

        blog_url = "{}/api/blogs/{}/post-list".format(root_m, blog_id)
        params = {
            'categoryNo': 0,
            'itemCount': 24,
            'page': 1,
            'userId': blog_id,
        }
        headers = {
            'Referer': '{}/{}?categoryNo=0&listStyle=post&tab=1'.format(root_m, blog_id),
        }

        site_req = Requests()
        url_list = []
        while True:
            blog = site_req.session.get(blog_url, headers=headers, params=params).json()

            for post in blog['result']['items']:
                log_no = post['logNo']
                post_url = "{}/PostView.naver?blogId={}&logNo={}".format(root, blog_id, log_no) 
                if post_url in url_list:
                    site_req.session.close()
                    break
                url_list.append(post_url)
            else:     
                if blog['result']['items'] == []:
                    site_req.session.close()
                    break
                params['page'] += 1
                continue
            break

        logger.log_info(f"Found {len(url_list)} post(s)")
        for i in url_list:
            yield from naverblog_post(i)

    def naverblog_series(hd):
        """Get series"""
        blog_id = hd.split('blogId=')[1].split('&')[0].strip('#')
        category_no = hd.split('categoryNo=')[1].split('&')[0].strip('#')

        series_url = "{}/PostTitleListAsync.naver".format(root)
        params = {
            'blogId': blog_id,
            'viewdate': '',
            'currentPage': 1,
            'categoryNo': category_no,
            'parentCategoryNo': '',
            'countPerPage': '25'
        }

        site_req = Requests()
        url_list = []
        while True:
            series = site_req.session.get(series_url, params=params).text.replace('\\', '')
            json_data = json.loads(series)

            for post in json_data['postList']:
                log_no = post['logNo']
                post_url = "{}/PostView.naver?blogId={}&logNo={}".format(root, blog_id, log_no) 
                if post_url in url_list:
                    site_req.session.close()
                    break
                url_list.append(post_url)
            else:     
                params['currentPage'] += 1
                continue
            break

        logger.log_info(f"Found {len(url_list)} post(s)")
        for i in url_list:
            yield from naverblog_post(i)

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
        
        post_writer = (site.split(
            "meta property=\"naverblog:nickname\" content=\"")[1]
            .split("\"")[0]).strip()
        post_series = (re.sub(
                r'<a[^>]*>(.*?)</a>', lambda match: match.group(1), site.split(
                    '<div class="blog2_series">')[1]
                .split('</div>')[0]).strip())
        post_title = (site.split(
            "meta property=\"og:title\" content=\"")[1].split("\"")[0].strip())
        post_date = (re.search(
            r'<span class="[^"]*se_publishDate[^"]*">(.*?)</span>', site).group(1).strip())
        if '시간' in post_date:
            import pytz
            kst = pytz.timezone('Asia/Seoul')
            hours = int(re.search(r'(\d+)', post_date).group(1))
            post_date = datetime.datetime.now(kst) - datetime.timedelta(hours=hours)
        elif '분' in post_date:
            import pytz
            kst = pytz.timezone('Asia/Seoul')
            minutes = int(re.search(r'(\d+)', post_date).group(1))
            post_date = datetime.datetime.now(kst) - datetime.timedelta(minutes=minutes)
        else:
            post_date = datetime.datetime.strptime(post_date, '%Y. %m. %d. %H:%M')
        
        post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        # Get Image from Post
        pattern = re.compile(r"data-linkdata='([^']+)'")
        matches = pattern.finditer(site)
        index = '001'
        for match in matches:
            try:
                linkdata = json.loads(match.group(1))
                if 'src' in linkdata and 'storep' not in linkdata['src']:
                    src = str(linkdata['src'].split('?')[0].strip('\'"')).replace('postfiles', 'blogfiles')
                    if src is None or src == '':
                        continue
                    if re.search(r'%[1-9A-Z]',src) is None:
                        img_list.append((src, index))
                        index = str(int(index) + 1).zfill(3)
                        continue

                    img_list.append(src)
            except json.JSONDecodeError as e:
                logger.log_error(f"Error decoding JSON: {e}")

        # Get Image from header
        pattern_h = re.compile(r'style="background-image:url\(([^)]+)\)')
        matches = pattern_h.findall(site)
        for match in matches:
            src = str(match.split('?')[0].strip('\'"')).replace('postfiles', 'blogfiles')
            img_list.append(src)

        # Get Video from Post        
        for match in re.compile(r"data-module='([^']+)'").finditer(site):
            if 'v2_video' not in match.group(1):
                continue
            logger.log_info("Extracting video from post")
            j = json.loads(match.group(1))
            video_id = j['id']
            media = j['data']
            video_api = 'https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}'.format(media['vid'])
            params = {
                'key': media['inkey'],
                'sid': 2,
                'pid': video_id,
                'nonce': Misc.get_time(),
                'devt': 'html5_pc',
                'prv': 'N',
                'aup': 'N',
                'stpb': 'N',
                'cpl': 'ko_KR',
                'providerEnv': 'real',
                'adt': 'glad',
                'lc': 'ko_KR',
            }
            video_url = site_req.session.get(video_api, params=params).json()
            video = max(video_url['videos']['list'], key=lambda x: x.get('size'), default=None)
            img_list.append((video['source'], video_id))

        site_req.session.close()
        logger.log_extractor_info(
            f"Writer: {post_writer}",
            f"Series: {post_series}",
            post_title,
            post_date,
            img_list
        )

        dir = [SITE_INFO.name, post_writer, post_series,
               f"{post_date_short} {post_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option='naverblog',
            custom_headers={'Referer': '{}'.format(root)}
        )

        yield payload


    if (re.search(postlist_pattern, hd)):
        logger.log_info("Naver Blog Series")
        yield from naverblog_series(hd)
    elif (re.search(postview_pattern, hd)):
        logger.log_info("Naver Blog Post")
        yield from naverblog_post(hd)
    elif (re.search(blog_pattern, hd)):
        logger.log_info("Naver Blog Main Page")
        yield from naverblog_blog(hd)