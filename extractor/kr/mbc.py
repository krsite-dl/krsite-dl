import datetime

from common.common_modules import SiteRequests
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="mbc.co.kr", name="MBC")

def get_data(hd):
    idx = hd.split('idx=')[-1].split('&')[0]
    api = f'https://mbcinfo.imbc.com/api/photo/m_info?intIdx={idx}'
    img_api = f'https://mbcinfo.imbc.com/api/download?file='

    site_req = SiteRequests()
    r = site_req.session.get(api)
    json_data = r.json()

    post_title = json_data['list'][0]['title']
    post_date = json_data['list'][0]['reg_dt']
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    post_date_short = post_date.strftime('%y%m%d')

    img_list = []

    for i in json_data['list']:
        img_list.append(f"{img_api}{i['photo_fullpath']}")

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)

    print("Found %s image(s)" % len(img_list))
    
    dir = [SITE_INFO.name, f"{post_date_short} {post_title}"]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)