"""Extractor for https://genie.co.kr"""

from utils.core import (
    urlparse,
    Requests, 
    SiteParser,
    Logger, 
    Site,
    DataPayload,
    re,
    datetime, 
    )

SITE_INFO = Site(hostname="genie.co.kr", name="Genie")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    hostname = urlparse(hd).hostname

    site_parser = SiteParser()
    site_req = Requests()

    def genie_artist(hd):
        r = site_req.session.get(hd).text

        artist_edm_release = r.split(
            'artist-edm-list-insert">')[1].split('</div>')[0]

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
        artist = r.split("meta property=\"og:title\" content=\"")[
            1].split("\"")[0].strip(" - genie")
        logger.log_info(f"Artist: {artist}")
        logger.log_info(f"Found {len(magazine_list)} magazine(s)")
        for i in magazine_list:
            genie_magazine(i, artist)

    def genie_magazine(data, *args):
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

        site_req.session.close()
        logger.log_extractor_info(
            mag_title, 
            mag_date, 
            img_list
        )

        artist = args[0]

        dir = [SITE_INFO.name, f"{artist}", f"{mag_date_short} {mag_title}"]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option=None,
            custom_headers=None
        )

        yield payload

    if f"{hostname}/detail/artistInfo" in hd:
        logger.log_info("From Artist")
        yield from genie_artist(hd)
