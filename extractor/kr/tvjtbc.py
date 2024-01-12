import datetime

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, DataPayload

SITE_INFO = Site(hostname="tv.jtbc.co.kr", name="JTBC TV", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    soup = site_parser._parse(site_requests.session.get(hd).text)

    post_title = soup.find('h3', class_='veiw_tit').text.strip()
    post_date = soup.find('div', class_='view_info_txt').find_all('span')[2].text.replace('-', '')
    post_date_short = post_date[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %p %I:%M:%S')
    content = soup.find('div', class_='view_cont_txt')

    img_list = []

    for item in content.findAll('img'):
        img_list.append(item.get('src'))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir = [SITE_INFO.name, post_date_short, post_title]

    payload = DataPayload(
        directory_format=dir,
        media=img_list,
        option=None,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(payload)