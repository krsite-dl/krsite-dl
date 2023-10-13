import requests
import re

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup

def from_melon(hd, loc, folder_name):
    img_list = []
    artist_id = re.search(r'(?<=artistId=)\d+', hd).group(0)

    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()

    print(post_title)

    init_url = f'https://www.melon.com/artist/photoPaging.htm?startIndex=1&pageSize=5000&orderBy=NEW&listType=0&artistId={artist_id}'

    r = requests.get(init_url, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    photo_list = soup.find('div', class_='photo_list')

    for item in photo_list.findAll('img'):
        img_list.append(re.sub(r'(?<=.jpg).*$', '', item['src']))

    print("Found %s image(s)" % len(img_list))

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, None, None, loc, folder_name)