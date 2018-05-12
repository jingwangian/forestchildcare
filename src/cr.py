#!/usr/bin/env python3


import os
import time
import requests
import logging
import argparse
import re

# proxies = {'http':'127.0.0.1:3128','https':'127.0.0.1:3128'}
proxies = None

# 30second for request time out
request_time_out = 10

base_url = 'http://www.forestchildcare.com.au'
main_page_url = base_url + '/platypus-news.html'
cookies = {'cookies': '''is_mobile=0; language=en; _sp_ses.0176=*; _snow_ses.f0ec=*; __qca=P0-664616487-1519037502123; WeeblySiteLogin=weeblylogin:be8f35e32a9303071ae01284e2a16aa6430656af523ba86b072a8c6225ca451e; _sp_id.0176=c5594888-2dab-46ad-b3f7-d307e79f6cd3.1519037502.1.1519038400.1519037502.27e6d773-7875-4a55-a5ee-b0f8e0c0580e; _snow_id.f0ec=0a838518-0eb7-4e5b-802b-a33e2c98008d.1519037502.1.1519038400.1519037502.381d9e5c-f28a-40c1-9398-08c952c38461'''}

download_dir = '../downloads'

# print(cookies)


def get_img_list(content):
    img_list = []

    img_list = re.findall(rb"(/uploads[/\d+]+img-\d{4}\.jpg)", content)

    img_list.sort()

    img_list = ['http://www.forestchildcare.com.au{}'.format(x.decode()) for x in img_list]

    l2 = get_img_list_2(content)

    l2.sort()

    img_list.extend(l2)

    return {x.replace('.jpg', '_orig.jpg') for x in img_list}


def get_img_list_2(content):
    # img_list = re.findall(rb"/2\\/3\\/6\\/6\\/23669552\\(/img-\d{4}_\d{1}_orig\.jpg)", content)
    img_list = re.findall(rb"uploads.*?\.jpg", content)

    # img_list = ['http://www.forestchildcare.com.au/uploads/2/3/6/6/23669552{}'.format(x.decode()) for x in img_list]

    img_list = ['http://www.forestchildcare.com.au/{}'.format(x.decode()) for x in img_list]

    return img_list


def download_img(img_url):
    file_name = os.path.basename(img_url)
    full_file_name = os.path.join(download_dir, file_name)

    if not os.path.isfile(full_file_name):
        r = requests.get(img_url, proxies=proxies, timeout=request_time_out, cookies=cookies)
        if r.status_code == 200:
            with open(full_file_name, 'wb') as fd:
                fd.write(r.content)
                print("Downloaded the {}".format(file_name))
    else:
        print("{} is already exist".format(full_file_name))


def send_request(url):
    print(url)
    r = requests.get(url, proxies=proxies, timeout=request_time_out, cookies=cookies)

    if r.status_code == 200:
        # print(r.content)
        img_list = get_img_list(r.content)

        [print(x) for x in img_list]

        [download_img(x) for x in img_list]


def test_case1():
    with open('a.txt', 'rb') as f:
        img_list = get_img_list(f.read())

        [(print(x), print('\n')) for x in img_list]


def test_case2():
    content = b'''<meta property="og:image" content="http://www.forestchildcare.com.au/uploads/2/3/6/6/23669552/img-8943.jpg" />'''

    img_list = get_img_list(content)

    [print(x) for x in img_list]


def test_case3():
    content = b'''images:[{"url":"2\\/3\\/6\\/6\\/23669552\\/img-8943.jpg","width":400,"height":300,"fullHeight":800,"fullWidth":1067},{"url":"2\\/3\\/6\\/6\\/23669552\\/img-8944.jpg","width":400,"height":300,"fullHeight":800,"fullWidth":1067},{"url":"2\\/3\\/6\\/6\\/23669552\\/img-8945.jpg","width":400,"height":300,"fullHeight":800,"fullWidth":1067},{"url":"2\\/3\\/6\\/6\\/23669552\\/img-8946.jpg","width":400,"height":300,"fullHeight":800,"fullWidth":1067},{
    '''
    img_list = get_img_list(content)

    [print(x) for x in img_list]


def main():
    #     get_urls(2000,1,1,10)
    # test_case1()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('url', help='url')
    # parser.add_argument('--output', help='output file name')

    # args = parser.parse_args()

    # url = args.url
    send_request(main_page_url)


if __name__ == '__main__':
    main()
