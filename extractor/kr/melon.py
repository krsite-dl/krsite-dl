import requests
import datetime
import re

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="melon.com", name="Melon", location="KR")

def get_data(hd):
    img_list = []
    artist_id = re.search(r'(?<=artistId=)\d+', hd).group(0)

    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()

    init_url = f'https://www.melon.com/artist/photoPaging.htm?startIndex=1&pageSize=5000&orderBy=NEW&listType=0&artistId={artist_id}'

    r = requests.get(init_url, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    photo_list = soup.find('div', class_='photo_list')

    for item in photo_list.findAll('img'):
        img_list.append(re.sub(r'(?<=.jpg).*$', '', item['src']))
    
    print("Title: %s" % post_title)
    print("Found %s image(s)" % len(img_list))

    substitute_date = datetime.datetime.now()
    payload = ScrapperPayload(
        title=post_title,
        shortDate=None,
        mediaDate=None,
        site=SITE_INFO.name,
        series=None,
        writer=None,
        location=SITE_INFO.location,
        media=img_list,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)