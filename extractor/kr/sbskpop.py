import requests
import datetime

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup


def from_sbskpop(hd, loc, folder_name):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:description')['content'].strip()
    post_date = datetime.datetime.strptime(post_title[:8], '%y.%m.%d')
    post_date_short = post_date.strftime('%Y%m%d')[2:]

    content = soup.find('div', class_='page-content')

    img_list = []

    for img in content.findAll('img'):
        srcset_attrs = ['data-srcset', 'srcset']
        for srcset_attr in srcset_attrs:

            srcset_value = img.get(srcset_attr)
            if srcset_value:

                sources = srcset_value.split(',')
                if sources and sources[-1] == '':
                    sources.pop()
                max_source = max(
                    sources, 
                    key=lambda s: int(s.strip().split(' ')[-1][:-1]), default=None
                )
                # print(max_source)

                if max_source:
                    highest_width_url = max_source.strip().split(' ')[0]

                    if highest_width_url:
                        # print(highest_width_url)
                        img_list.append(highest_width_url)

    print("Post title: %s" % post_title)
    print("Post date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    # print(img_list)

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, post_title, post_date, post_date_short, loc, folder_name)