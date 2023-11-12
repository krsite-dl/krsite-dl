import requests
import datetime

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="tv.jtbc.co.kr", name="JTBC TV", location="KR")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

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

    payload = ScrapperPayload(
        title=post_title,
        shortDate=post_date_short,
        mediaDate=post_date,
        site=SITE_INFO.name,
        series=None,
        writer=None,
        location=SITE_INFO.location,
        media=img_list,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory_alternate(payload)