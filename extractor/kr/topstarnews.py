import requests
import datetime

from rich import print
from pytz import timezone
from urllib.parse import urlparse, parse_qs, urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from common.common_modules import SiteRequests, SiteParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="topstarnews.net", name="Topstarnews", location="KR")

def get_data(hd):
    site_parser = SiteParser()
    site_requests = SiteRequests()
    
    def iterate_pages():
        soup = site_parser._parse(site_requests.session.get(hd).text)

        pagination = soup.find('ul', class_='pagination')

        first_page = pagination.find('li', class_='pagination-start')
        base = 'https://topstarnews.net/news' + first_page.find('a').get('href').strip('.')

        # get page value from url
        query_params = parse_qs(urlparse(hd).query)
        page = lambda: int(query_params.get('page')[0]) if query_params.get('page') else 1
        # start iterating
        while True:
            print(f"Page {page()}")
            query_params['page'] = [str(page)]
            new_query_string = urlencode(query_params, doseq=True)
            new_url = urlparse(base)._replace(query=new_query_string).geturl()
            # print(new_url)
            grab_post_urls(new_url)
            page += 1

            # stop if there's no post in the page
            if soup.find('div', class_='article-column') is None:
                break


    def grab_post_urls(page_url):
        soup = site_parser._parse(site_requests.session.get(hd).text)

        section = soup.find('section', class_='article-custom-list')

        post_urls = []

        for item in section.findAll('div', class_='article-column'):
            post_urls.append('https://topstarnews.net' + item.find('a').get('href'))
        
        print('Found %s post(s)' % len(post_urls))

        for post in post_urls:
            post_page(post)


    def post_page(hd):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        soup = site_parser._parse(site_requests.session.get(hd).text)

        post_title = soup.find('meta', property='og:title')['content'].strip()
        post_dates = soup.find_all('meta', property='article:published_time')
        if len(post_dates) >= 2:
            post_date = post_dates[1].attrs['content']
        else:
            post_date = post_dates[0].attrs['content']

        post_date_short = post_date.replace('-', '')[2:8]
        post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
        tz = timezone('Asia/Seoul')
        post_date = post_date.astimezone(tz).replace(tzinfo=None)
        
        img_list = []

        content = soup.find('div', itemprop='articleBody')

        for item in content.findAll('img'):
            img_list.append(item.get('data-org'))

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

        DirectoryHandler().handler_directory_combine(payload)
        
    if 'idxno' in hd:
        print('[yellow]Single page[/yellow]')
        post_page(hd)
    else:
        print('[yellow]Iterating pages[/yellow]')
        iterate_pages()