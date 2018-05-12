#!/usr/bin/env python3

import os
import datetime
import requests

from html.parser import HTMLParser
from typing import List


class ForestPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.host_name = "http://www.forestchildcare.com.au"
        self.dir_name = "/uploads"

        self.current_tag = ''
        self.in_javascript = False
        self.jpgs_in_script = []
        self.pic_list = []
        self.final_pic_list = []

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        for attr in attrs:
            if '.jpg' in attr[1]:
                self.pic_list.append(attr[1])
            elif "text/javascript" in attr[1]:
                if tag == 'script':
                    self.in_javascript = True

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.in_javascript = False

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        if self.in_javascript:
            self.handle_data_in_script(data)

    def handle_data_in_script(self, script_content):
        lines = script_content.split(',')

        for line in lines:
            if ".jpg" in line and '"url":' in line:
                url = self.get_pic_in_url(line)
                if url:
                    self.pic_list.append(url)

    def get_pic_in_url(self, data):
        """
        Get jpg url from data like : images:[{"url":"2\/3\/6\/6\/23669552\/img-2295.jpg"
        """
        try:
            jpg_url = data.split('"url":')[1]
        except IndexError:
            return None

        jpg_url = jpg_url.replace("\/", "/")
        if jpg_url[0] == '"':
            jpg_url = jpg_url[1:-1]

        return jpg_url

    def adjust_one_pic_url(self, pic_url):
        """
        """
        final_url = None
        pic_url = pic_url.replace('_orig.jpg', '.jpg')

        if pic_url.startswith("http://"):
            final_url = pic_url
        elif pic_url.startswith(self.dir_name):
            final_url = self.host_name + pic_url
        elif str.isnumeric(pic_url[0]):
            final_url = self.host_name + self.dir_name + "/" + pic_url

        if final_url and 'uploads' in final_url:
            final_url = final_url.replace('_orig.jpg', '.jpg')
            return final_url

    def adjust_all_pic_url(self) -> List:
        """
        Return a new list contains adjusted pic url
        """
        final_url_list = set()
        for url in self.pic_list:
            final_url = self.adjust_one_pic_url(url)
            if final_url:
                final_url_list.add(final_url)

        return list(sorted(final_url_list))

    def get_all_pic_urls(self, data) -> List:
        self.feed(data)
        self.final_pic_list = self.adjust_all_pic_url()

        return self.final_pic_list


class ForestWebPage:
    def __init__(self, download_dir='downloads'):
        self.content = None
        self.download_dir = os.path.join(download_dir, str(datetime.date.today()))
        self.http_url_host = "http://www.forestchildcare.com.au"

        if not os.path.isdir(self.download_dir):
            os.mkdir(self.download_dir)

    def request(self, http_url, cookies=None):
        return requests.get(http_url)

    def request_with_password(self, http_url, password):
        headers = {'Host': 'www.forestchildcare.com.au'}
        payload = {"redirect": "/platypus-news.html"}
        data = {"p": password, "redirect": "/platypus-news.html", "u": "weebs"}

        return requests.post(http_url, headers=headers, params=payload, data=data)

    def get_page_content(self, page_name="platypus-news.html"):
        http_url = os.path.join(self.http_url_host, page_name)

        r = self.request(http_url)
        if 'This area is password protected' in r.text:
            r = self.request_with_password(http_url='http://www.forestchildcare.com.au/401/login.php',
                                           password='intouch')

            self.content = r.text

        return self.content

    def download_img(self, img_url):
        file_name = os.path.basename(img_url)
        full_file_name = os.path.join(self.download_dir, file_name)

        if not os.path.isfile(full_file_name):
            print("downloading {} ".format(img_url), end='  -----  ')
            r = self.request(img_url.replace(".jpg", "_orig.jpg"))

            if r.status_code == 200:
                self.save_img(full_file_name, r.content)
                print("Ok")
            else:
                r = self.request(img_url)
                if r.status_code == 200:
                    self.save_img(full_file_name, r.content)
                    print("Ok")
                else:
                    print("Failed")

        else:
            print("{} is already downloaded".format(img_url))

    def save_img(self, file_name, content):
        with open(file_name, 'wb') as fd:
            fd.write(content)


def main():
    page = ForestWebPage(download_dir="../downloads")

    content = page.get_page_content("platypus-news.html")

    parser = ForestPageParser()
    pic_url_list = parser.get_all_pic_urls(content)

    [page.download_img(pic_url) for pic_url in pic_url_list]

    print("Total {} img downloaded".format(len(pic_url_list)))


if __name__ == '__main__':
    main()
