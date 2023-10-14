import requests
import datetime
import re

from client.user_agent import InitUserAgent
from rich import print
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def from_genie(hd, loc, folder_name):
    hostname = urlparse(hd).hostname
    def genie_artist():
        r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})

        soup = BeautifulSoup(r.text, 'html.parser')

        artist_edm_release = soup.find('div', class_='artist-edm-list-insert')


        magazine_list = []

        for li in artist_edm_release.find_all('li'):
            p = li.find_all('p')
            magazine_date = p[0].text.strip()
            magazine_title = p[1].text.strip()
            magazine_list.append([magazine_date, magazine_title, f"https://{hostname}{li.find('a')['href']}"])


        print("Artist: %s" % soup.find('meta', property='og:title')['content'].strip().replace(' - genie', ''))
        print("Found %s magazine(s)" % len(magazine_list))

        for i in magazine_list:
            genie_magazine(i)


    def genie_magazine(data):
        mag_date, mag_title, mag_url = data

        r = requests.get(mag_url, headers={'User-Agent': InitUserAgent().get_user_agent()})
        soup = BeautifulSoup(r.text, 'html.parser')

        magazine_view = soup.find('div', class_='magazine-view')

        image_list = []
        for image in magazine_view.find_all('img'):
            image = re.sub(r'(?<=.jpg).*$', '', image['src'])
            image_list.append(f"https:{image}")
        
        mag_date = datetime.datetime.strptime(mag_date, '%Y.%m.%d')
        mag_date_short = mag_date.strftime('%y%m%d')

        print("Title: %s" % mag_title)
        print("Date: %s" % mag_date)
        print("Found %s image(s)" % len(image_list))

        from down.directory import DirectoryHandler

        DirectoryHandler().handle_directory(image_list, mag_title, mag_date, mag_date_short, loc, folder_name)
        

    if f"{hostname}/detail/artistInfo" in hd:
        print("[bold blue]From Artist[/bold blue]")
        genie_artist()