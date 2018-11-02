# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Yao'

import requests
import urllib.request
import csv
import http
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


# 获取网页源代码
def gethtml(url):
    page = requests.get(url)
    page.encoding='utf-8'
    return page.text

# 解析出网站名称和URL
def urlparse(urllist,html):
   soup = BeautifulSoup(html,'lxml')
   for tag in soup.find_all('div',class_='CentTxt'):
       s_name = tag.find('a',class_='pr10 fz14').get_text()
       s_url = tag.find('span', class_='col-gray').get_text()
       f_url = 'http://' + s_url
       check = urllib.request.Request(f_url, headers = headers)
       try:
           check1 = urllib.request.urlopen(check)
           f = str(check1.geturl())
       except urllib.error.URLError as e:
           print(e.reason)
#           return None
       except http.client.RemoteDisconnected as e:
           print('RemoteDisconnected : ', e)
#           return None
       if 'http://' in f:
           urllist.append([s_name, f])
       else:
           print(f)


# 主函数，用于生成csv
def main():
    with open('url.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['网站名称', 'URL'])
        for page in range(2, 40):
            ul = []
            url = 'http://top.chinaz.com/hangye/index_' + str(page) + '.html'
            html = gethtml(url)
            urlparse(ul, html)
            writer.writerows(ul)
        csvfile.close()

main()
