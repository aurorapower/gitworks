#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import re
import os
import urllib
import gzip
from urllib.request import urlopen
from io import StringIO
from bs4 import BeautifulSoup

DOMAIN = 'https://t66y.com/'
__USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

def __trans_code(response):
    return __unzip(response.read()).decode('gbk').encode('utf-8')


def __unzip(data):
    data = io.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data

def fetch(url):
    request = urlopen.Request(url)
    request.add_header('User-Agent', __USER_AGENT)
    request.add_header('Accept-Encoding', 'gzip, deflate')
    return __trans_code(urlopen.urlopen(request))

def __get_href_and_title(line):
    line_xml = BeautifulSoup(line, 'html.parser')
    return line_xml.h3.a['href'], line_xml.h3.string

def __get_content(html, title):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_='tpc_content do_not_catch').get_text(strip=True).encode('utf8')
    if not os.path.exists('files'):
        os.mkdir('files')
    porn_article = open('files/' + title + '.txt', 'w+')
    porn_article.write(content)
    porn_article.close()

def __get_article(line):
    href, title = __get_href_and_title(line)
    if 'htm_data' in href:
        article_url = http.DOMAIN + href
        html = http.fetch(article_url)
        __get_content(html, title)

articles = open('articles.txt', '+a')
for url_tag in articles.readlines():
    __get_article(url_tag)

PORN_HOME_PAGE_URL = http.DOMAIN + 'thread0806.php'

url = PORN_HOME_PAGE_URL + '?fid=20&search=&page=1'
soup = BeautifulSoup(http.fetch(url), 'html.parser')
page_button = soup.find(id='last').find_previous_sibling().find_previous_sibling()
button_value = page_button.input['value']
max_page_number = int(re.split('/', button_value)[1])

articles = open('articles.txt', 'a+')
for index in range(1, max_page_number + 1):
    print ('current page is %d' % index)
    url = PORN_HOME_PAGE_URL + '?fid=20&search=&page=' + str(index)
    soup = BeautifulSoup(http.fetch(url), 'html.parser')
    items = soup.find_all('h3')
    text = '\n'.join(str(tag) for tag in items)
    articles.write(text)

articles.close()