import datetime

from common.common_modules import SeleniumParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="mbc.co.kr", name="MBC", location="KR")

def get_data(hd):
    parser = SeleniumParser()

    def mbc_post(hd):
        w = parser._requests(hd)

        post_title = w.find_element(parser.get_by('TAG_NAME'), 'h2').text
        post_date = w.find_element(parser.get_by('CLASS_NAME'), 'date').text
        post_date_short = post_date.replace('/', '')[2:8]
        date_a = post_date[:10]
        date_b = post_date[-5:]
        post_date = datetime.datetime.strptime(f"{date_a} {date_b}", '%Y/%m/%d %H:%M')

        img_list = []

        print("Title: %s" % post_title)
        print("Date: %s" % post_date)

        for i in w.find_element(parser.get_by('CLASS_NAME'), 'img_down').find_elements(parser.get_by('TAG_NAME'), 'a'):
            img_list.append(i.get_attribute('href'))

        w.quit()

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

        DirectoryHandler().handle_directory(payload)


    mbc_post(hd)
