import datetime
import time
import re

from rich import print
from selenium.common.exceptions import NoSuchElementException

from common.common_modules import SeleniumParser
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="post.naver.com", name="Naver Post", location="KR")


def get_data(hd):
    BASE = r"(?:https?://)?(?:m\.)?(post\.naver\.com)"
    pattern = BASE + r"(/my.)?(?:naver|nhn)"
    pattern2 = BASE + r"(/search/authorPost.)?(?:naver|nhn)"
    pattern3 = BASE + r"(/series.)?(?:naver|nhn)"
    pattern4 = BASE + r"(/my/series/detail.)?(?:naver|nhn)"
    pattern5 = BASE + r"(/viewer/postView.)?(?:naver|nhn)"

    def naverpost_search(hd):
        parser = SeleniumParser()
        w = parser._requests(hd)

        post_list = set()

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'link_end'):
                    post_list.add(i.get_attribute('href'))
        
        w.quit()
        print("Found %s post(s)" % len(post_list))

        for i in post_list:
            naverpost_post(i)


    def naverpost_series(hd):
        parser = SeleniumParser()
        w = parser._requests(hd)

        series_list = set()
        
        sender_name = w.find_element(parser.get_by('CLASS_NAME'), 'name').text
        print("Sender: %s" % sender_name)

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'link'):
                    series_list.add(i.get_attribute('href'))
        
        w.quit()
        print("Found %s series" % len(series_list))
        print("------------------\n")

        for i in series_list:
            naverpost_list(i)


    def naverpost_list(hd):
        parser = SeleniumParser()
        w = parser._requests(hd)
        
        post_list = set()

        btn = w.find_element(parser.get_by('CLASS_NAME'), '_more')
        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False
                for i in w.find_elements(parser.get_by('CLASS_NAME'), 'spot_post_area'):
                    post_list.add(i.get_attribute('href'))

        w.quit()
        print("Found %s post(s)" % len(post_list))
        
        for i in post_list:
            naverpost_post(i)


    def naverpost_post(hd):
        parser = SeleniumParser()
        w = parser._requests(hd)

        try:
            post_writer = w.find_element(parser.get_by('CLASS_NAME'), 'se_author').text
            post_series = w.find_element(parser.get_by('CLASS_NAME'), 'se_series').text[3:]
            post_title = w.find_element(parser.get_by('CLASS_NAME'), 'se_textarea').text.replace('\n', ' ')
            post_date = w.find_element(parser.get_by('XPATH'), '//meta[@property="og:createdate"]') # using meta tag for more accurate time
            post_date = datetime.datetime.strptime(post_date.get_attribute('content'), '%Y.%m.%d. %H:%M:%S')
            post_date_short = post_date.strftime('%y%m%d')
        except NoSuchElementException:
            post_writer = w.find_element(parser.get_by('CLASS_NAME'), 'writer.ell').text
            post_series = w.find_element(parser.get_by('CLASS_NAME'), 'series').text
            post_title = w.find_element(parser.get_by('CLASS_NAME'), 'title').text.replace('\n', ' ')
            post_date = w.find_element(parser.get_by('XPATH'), '//meta[@property="og:createdate"]') # using meta tag for more accurate time
            post_date = datetime.datetime.strptime(post_date.get_attribute('content'), '%Y.%m.%d. %H:%M:%S')
            post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        print("\nSeries: %s" % post_series)
        print("Title: %s" % post_title)
        print("Date: %s" % post_date_short)
        print("Writer: %s" % post_writer)
        
        for i in w.find_elements(parser.get_by('CLASS_NAME'), 'se_mediaImage'):
            if 'storep' not in i.get_attribute('src'):
                img_list.append(str(i.get_attribute('src').split('?')[0]))

        for i in w.find_elements(parser.get_by('CLASS_NAME'), 'img_attachedfile'):
            if 'storep' not in i.get_attribute('src'):
                img_list.append(str(i.get_attribute('src').split('?')[0]))

        for i in w.find_elements(parser.get_by('CLASS_NAME'), 'se_card_exception_img'):
            if 'storep' not in i.get_attribute('src'):
                img_list.append(str(i.get_attribute('src').split('?')[0]))

        w.quit()

        print("Found %s image(s)" % len(img_list))

        payload = ScrapperPayload(
            title=post_title,
            shortDate=post_date_short,
            mediaDate=post_date,
            site=SITE_INFO.name,
            series=post_series,
            writer=post_writer,
            location=SITE_INFO.location,
            media=img_list,
        )

        from down.directory import DirectoryHandler

        DirectoryHandler().handle_directory_naver(payload)
    
        
    if re.search(pattern, hd):
        print("[bold green]Naver Post Main Page[/bold green]")
        naverpost_search(hd)

    elif re.search(pattern2, hd):
        print("[bold green]Naver Post Search Result[/bold green]")
        naverpost_search(hd)

    elif re.search(pattern3, hd):
        print("[bold green]Naver Post Series Page[/bold green]")
        naverpost_series(hd)

    elif re.search(pattern4, hd):
        print("[bold green]Naver Post Series List[/bold green]")
        naverpost_list(hd)

    elif re.search(pattern5, hd):
        print("[bold green]Naver Post Page[/bold green]")
        naverpost_post(hd)