import re

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="melon.com", name="Melon", location="KR")

def get_data(hd):
    img_list = []
    artist_id = re.search(r'(?<=artistId=)\d+', hd).group(0)

    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)


    post_title = soup.find('meta', property='og:title')['content'].strip()

    init_url = f'https://www.melon.com/artist/photoPaging.htm?startIndex=1&pageSize=5000&orderBy=NEW&listType=0&artistId={artist_id}'

    soup = site_parser._parse(site_requests.session.get(init_url).text)

    photo_list = soup.find('div', class_='photo_list')

    for item in photo_list.findAll('img'):
        img_list.append(re.sub(r'(_\d+)(?=\.jpg)', '_org', re.sub(r'(?<=.jpg).*$', '', item['src'])))
    
    print("Title: %s" % post_title)
    print("Found %s image(s)" % len(img_list))
    
    dir = [SITE_INFO.name, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)