import requests
import datetime
import time
from rich import print
from pytz import timezone
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode
import down.directory as dir

def from_topstarnews(hd, loc, folder_name):
    def iterate_pages():
        r = requests.get(hd, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'})
        soup = BeautifulSoup(r.text, 'html.parser')

        pagination = soup.find('ul', class_='pagination')

        first_page = pagination.find('li', class_='pagination-start')
        base = 'https://topstarnews.net/news' + first_page.find('a').get('href').strip('.')

        # start iterating
        page = 1
        while True:
            print('Page %s' % page)
            query_params = parse_qs(urlparse(base).query)
            query_params['page'] = [str(page)]
            new_query_string = urlencode(query_params, doseq=True)
            new_url = urlparse(base)._replace(query=new_query_string).geturl()
            grab_post_urls(new_url)
            page += 1

            # stop if there's no post in the page
            if soup.find('section', class_='article-custom-list') is None:
                break


    def grab_post_urls(page_url):
        r = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'})
        soup = BeautifulSoup(r.text, 'html.parser')

        section = soup.find('section', class_='article-custom-list')

        post_urls = []

        for item in section.findAll('div', class_='article-column'):
            post_urls.append('https://topstarnews.net' + item.find('a').get('href'))
        
        print('Found %s post(s)' % len(post_urls))

        for post in post_urls:
            post_page(post, loc, folder_name)
        
        time.sleep(15)


    def post_page(hd, loc, folder_name):
        r = requests.get(hd, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'})
        soup = BeautifulSoup(r.text, 'html.parser')

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

        dir.dir_handler_no_folder(img_list, post_title, post_date_short, post_date, loc, folder_name)

    
    if 'idxno' in hd:
        print('[yellow]Single page[/yellow]')
        post_page(hd, loc, folder_name)
    else:
        print('[yellow]Iterating pages[/yellow]')
        iterate_pages()