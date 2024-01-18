"""Extractor for https://genie.co.kr"""

import datetime
import re

from rich import print
from urllib.parse import urlparse
from common.common_modules import Requests, SiteParser
from common.data_structure import Site, DataPayload
from down.directory import DirectoryHandler

SITE_INFO = Site(hostname="genie.co.kr", name="Genie")


def get_data(hd):
    """Get data"""
    hostname = urlparse(hd).hostname

    site_parser = SiteParser()
    site_req = Requests()

    def genie_artist(hd):
        r = site_req.session.get(hd).text

        artist_edm_release = r.split('artist-edm-list-insert">')[1].split('</div>')[0]

        magazine_list = set()

        pattern = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL)
        matches = pattern.findall(artist_edm_release)
        for match in matches:
            href_p = re.compile(r'href="(.*?)"')
            href = href_p.findall(match)[0]
            date_p = re.compile(r'<p class="date">(.*?)</p>', re.DOTALL)
            date = date_p.findall(match)[0]
            title_p = re.compile(r'<p>(.*?)</p>')
            title = title_p.findall(match)[0]
            magazine_list.add((date, title, f"https://{hostname}{href}"))

        site_req.session.close()
        artist = r.split("meta property=\"og:title\" content=\"")[1].split("\"")[0].strip(" - genie")
        print(f"Artist: {artist}")
        print(f"Found {len(magazine_list)} magazine(s)")
        print(magazine_list)
        for i in magazine_list:
            genie_magazine(i)

    def genie_magazine(data):
        """Get magazine data"""
        mag_date, mag_title, mag_url = data

        soup = site_parser._parse(site_req.session.get(mag_url).text)

        magazine_view = soup.find('div', class_='magazine-view')

        img_list = []
        for image in magazine_view.find_all('img'):
            image = re.sub(r'(?<=.jpg).*$', '', image['src'])
            img_list.append(f"https:{image}")

        mag_date = re.sub(r'\s+', '', mag_date)
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
        genie_artist(hd)