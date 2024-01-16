"""Extractor for https://genie.co.kr"""

import datetime
import re

from rich import print
from urllib.parse import urlparse
from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="genie.co.kr", name="Genie")


def get_data(hd):
    """Get data"""
    hostname = urlparse(hd).hostname

    site_parser = SiteParser()
    site_requests = SiteRequests()

    def genie_artist():
        soup = site_parser._parse(site_requests.session.get(hd).text)

        artist_edm_release = soup.find('div', class_='artist-edm-list-insert')

        magazine_list = []

        for li in artist_edm_release.find_all('li'):
            p = li.find_all('p')
            magazine_date = p[0].text.strip()
            magazine_title = p[1].text.strip()
            magazine_list.append(
                [magazine_date, magazine_title,
                 f"https://{hostname}{li.find('a')['href']}"])

        print("Artist: %s" % soup.find('meta', property='og:title')
              ['content'].strip().strip(' - genie'))
        print("Found %s magazine(s)" % len(magazine_list))

        for i in magazine_list:
            genie_magazine(i)

    def genie_magazine(data):
        """Get magazine data"""
        mag_date, mag_title, mag_url = data

        soup = site_parser._parse(site_requests.session.get(hd).text)

        magazine_view = soup.find('div', class_='magazine-view')

        img_list = []
        for image in magazine_view.find_all('img'):
            image = re.sub(r'(?<=.jpg).*$', '', image['src'])
            img_list.append(f"https:{image}")

        mag_date = datetime.datetime.strptime(mag_date, '%Y.%m.%d')
        mag_date_short = mag_date.strftime('%y%m%d')

        print(f"Title: {mag_title}")
        print(f"Date: {mag_date}")
        print(f"Found {len(img_list)} image(s)")

        dir = [SITE_INFO.name, f"{mag_date_short} {mag_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option=None,
        )

        DirectoryHandler().handle_directory(payload)

    if f"{hostname}/detail/artistInfo" in hd:
        print("[bold blue]From Artist[/bold blue]")
        genie_artist()
