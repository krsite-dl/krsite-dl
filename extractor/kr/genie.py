import datetime
import re

from rich import print
from urllib.parse import urlparse
from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="genie.co.kr", name="Genie", location="KR")

def get_data(hd):
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
            magazine_list.append([magazine_date, magazine_title, f"https://{hostname}{li.find('a')['href']}"])


        print("Artist: %s" % soup.find('meta', property='og:title')['content'].strip().replace(' - genie', ''))
        print("Found %s magazine(s)" % len(magazine_list))

        for i in magazine_list:
            genie_magazine(i)


    def genie_magazine(data):
        mag_date, mag_title, mag_url = data

        soup = site_parser._parse(site_requests.session.get(hd).text)

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

        payload = ScrapperPayload(
            title=mag_title,
            shortDate=mag_date_short,
            mediaDate=mag_date,
            site=SITE_INFO.name,
            series=None,
            writer=None,
            location=SITE_INFO.location,
            media=image_list,
        )
        from down.directory import DirectoryHandler

        DirectoryHandler().handle_directory(payload)
        

    if f"{hostname}/detail/artistInfo" in hd:
        print("[bold blue]From Artist[/bold blue]")
        genie_artist()