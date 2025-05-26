"""Extractor for https://mikan-incomplete.com"""

from utils.core import (
    Requests, 
    Logger,  
    Site,
    DataPayload,
    re,
    json,
    datetime, 
    )

SITE_INFO = Site(hostname="mikan-incomplete.com", name="Mikan Times")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_req = Requests()
    site = site_req.session.get(hd).text
    
    json_raw = site.split('<script type="application/ld+json">')[1].split('</script>')[0]
    json_data = json.loads(json_raw)

    post_title = json_data['@graph'][3]['headline']
    post_date = json_data['@graph'][3]['datePublished']
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    post_date_short = post_date.strftime('%y%m%d')
    
    pattern = r'<figure class="wp-block-gallery.*?">(.*)<\/figure>'
    article = re.search(pattern, site, re.DOTALL).group(1)

    img_list = []

    pattern = re.compile(r'<img\s[^>]*>')
    matches = pattern.findall(article)
    for match in matches:
        img = match.split('src="')[1].split('"')[0]
        img_list.append(re.sub(r'(-\d+x\d+)(?=\.\w{3,4})', '', img))

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
