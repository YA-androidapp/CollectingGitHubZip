#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GitHubにある自分のリポジトリのZIPファイルを全取得する
#   (masterブランチ)
#############################################

# pip install beautifulsoup4
# pip install chardet

import bs4
import chardet
import os
import re
import sys
import urllib.request


# 作業フォルダ
dir_default = os.getcwd()
cd = os.path.expanduser('~\\OneDrive\\ドキュメント\\works\\Python\\GitHub')
# cd = os.path.dirname(os.path.abspath(__file__))


os.chdir(cd)
print(os.getcwd())


# 宣言
user = 'YA-androidapp'

url_top = 'https://github.com'
url_usertop = url_top + '/'+user+'?tab=repositories'

url_archive = '/archive/master.zip'

max = 3

# page
i = 0
for i in range(0, max, 1):
    i = i + 1
    url_post = '&page=' + str(i)
    print(str(i) + '\t / \t' + str(max) + '\t: ' + url_post + '\n', end='')

    try:
        request = urllib.request.urlopen(url_usertop + url_post)
        if(request.getcode() == 404):
            exit
        else:
            html_post = request.read()
            guess = chardet.detect(html_post)
            html_post = html_post.decode(guess['encoding'])
            soup = bs4.BeautifulSoup(html_post, 'lxml')

            html_list = soup.find('div', id='user-repositories-list')
            html_items = html_list.find_all('li')
            if(len(html_items) > 0):
                for html_item in html_items:
                    html_item_a = html_item.find('a')
                    html_item_link = html_item_a.get('href')
                    html_item_link = re.sub(r'[\r\n][ ]+', '', html_item_link)
                    html_item_title = ''
                    html_item_desc = ''

                    try:
                        html_item_title = html_item_a.text
                        html_item_desc = html_item.find(
                            'p', itemprop='description').text
                        html_item_title = re.sub(
                            r'[\r\n][ ]+', '', html_item_title)
                        html_item_desc = re.sub(
                            r'[\r\n][ ]+', '', html_item_desc)
                    except:
                        pass

                    print('\t' + url_top + html_item_link + '\t' +
                          html_item_title + '\t' + html_item_desc, end='')

                    html_item_fname = html_item_link.replace('/', '_')[1:]
                    html_item_fname += '_master.zip'  # masterブランチを狙いに行くので、gh-pagesしか切っていない場合に失敗する

                    is_failure = 'true'
                    try:
                        headers = {'Referer': url_top + html_item_link}
                        req = urllib.request.Request(
                            url_top + html_item_link + url_archive, headers=headers)
                        with urllib.request.urlopen(req) as response:
                            with open(html_item_fname, 'wb') as f:
                                f.write(response.read())
                        is_failure = 'false'
                    except:
                        print(sys.exc_info())

                    print('\t' + is_failure + '\n', end='')

                    try:
                        file_list_txt = open('list.txt', 'a')
                        file_list_txt.write(
                            url_top + html_item_link + '\t' + html_item_title + '\t' + html_item_desc + '\t' + is_failure + '\n')
                        file_list_txt.close()
                    except:
                        print(sys.exc_info())
    except:
        print(sys.exc_info())
    finally:
        os.chdir(dir_default)

print('DONE.')
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
