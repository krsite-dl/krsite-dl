"""Extractor for https://topstarnews.net/"""

from ..utils.core import (
    timezone,
    urlparse,
    urlencode,
    parse_qs,
    Requests, 
    SiteParser, 
    Logger, 
    Site,
    DataPayload,
    datetime, 
    )

SITE_INFO = Site(hostname="topstarnews.net", name="Topstarnews", location="KR")
logger = Logger('extractor', SITE_INFO.name)

def get_data(hd):
    """Get data"""
    site_parser = SiteParser()
    site_req = Requests()

    def iterate_pages():
        """Iterate pages until the end"""
        soup = site_parser._parse(site_req.session.get(hd).text)

        pagination = soup.find('ul', class_='pagination')

        first_page = pagination.find('li', class_='pagination-start')
        base = 'https://topstarnews.net/news' + \
            first_page.find('a').get('href').strip('.')

        # get page value from url
        query_params = parse_qs(urlparse(hd).query)
        def page(): return int(query_params.get('page')
                               [0]) if query_params.get('page') else 1
        # start iterating
        while True:
            logger.log_info(f"Page {page()}")
            query_params['page'] = [str(page)]
            new_query_string = urlencode(query_params, doseq=True)
            new_url = urlparse(base)._replace(query=new_query_string).geturl()
            grab_post_urls(new_url)
            page += 1

            # stop if there's no post in the page
            if soup.find('div', class_='article-column') is None:
                break

    def grab_post_urls(page_url):
        """Grab post urls from a page"""
        soup = site_parser._parse(site_req.session.get(hd).text)

        section = soup.find('section', class_='article-custom-list')

        post_urls = []

        for item in section.findAll('div', class_='article-column'):
            post_urls.append('https://topstarnews.net' +
                             item.find('a').get('href'))

        logger.log_info(f"Found {len(post_urls)} post(s)")

        for post in post_urls:
            yield from post_page(post)

    def post_page(hd):
        """Grab post data"""
        soup = site_parser._parse(site_req.session.get(hd).text)

        post_title = soup.find('meta', property='og:title')['content'].strip()
        post_dates = soup.find_all('meta', property='article:published_time')
        if len(post_dates) >= 2:
            post_date = post_dates[1].attrs['content']
        else:
            post_date = post_dates[0].attrs['content']

        post_date_short = post_date.replace('-', '')[2:8]
        post_date = datetime.datetime.strptime(
            post_date, '%Y-%m-%dT%H:%M:%S%z')
        tz = timezone('Asia/Seoul')
        post_date = post_date.astimezone(tz).replace(tzinfo=None)

        img_list = []

        content = soup.find('div', itemprop='articleBody')

        for item in content.findAll('img'):
            img_list.append(item.get('data-org'))

        logger.log_extractor_info(
            post_title, 
            post_date, 
            img_list
        )

        dir = [SITE_INFO.name, post_date_short]

        payload = DataPayload(
            directory_format=dir,
            media=img_list,
            option='combine',
            custom_headers=None
        )

        yield payload

    if 'idxno' in hd:
        logger.log_info('Single page')
        yield from post_page(hd)
    else:
        logger.log_info('Iterating pages')
        yield from iterate_pages()

    site_req.session.close()
