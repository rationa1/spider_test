# -*- coding: utf-8 -*-
# @Time : 2021/9/2 16:30
# @Author : rational
# @File : hgcg_spider.py
import requests
from fontTools.ttLib import TTFont
from xml import etree
from bs4 import BeautifulSoup
import re

url = 'http://hgcg.customs.gov.cn/hgcg/cggg/004001/MoreInfo.aspx?CategoryNum=004001'
header = {"Host": "hgcg.customs.gov.cn",
          "Connection": "keep-alive",
          "Content-Length": "13366",
          "Pragma": "no-cache",
          "Cache-Control": "no-cache",
          "Upgrade-Insecure-Requests": "1",
          "Origin": "http://hgcg.customs.gov.cn",
          "Content-Type": "application/x-www-form-urlencoded",
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
          "Referer": "http://hgcg.customs.gov.cn/hgcg/cggg/004001/MoreInfo.aspx?CategoryNum=004001",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Cookie": "ASP.NET_SessionId=suhtltz3nvcoyxnnn3yhyy55"}


def get_next_url(view):
    body_data = {"__VIEWSTATE": '',
                 "__EVENTTARGET": 'MoreInfoList1$Pager',
                 "__EVENTARGUMENT": '',  # 页码
                 "__VIEWSTATEENCRYPTED": '', }
    return


def dispose_data(res, rsp):
    soup = BeautifulSoup(rsp, "lxml")
    ressoup = soup.find_all("div", attrs={"id": "MoreInfoList1_Pager"})


def get_response(url):
    res = []
    response = requests.get(url)
    dispose_data(res, response)


def main(url):
    response = get_response(url)


if __name__ == '__main__':
    # main(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    ressoup = soup.find_all("input", attrs={"type": "hidden", "name": "__VIEWSTATE", "id": "__VIEWSTATE"})
    VIEWSTATE = ressoup[0].get("value")
    print(VIEWSTATE)

    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__EVENTTARGET': 'MoreInfoList1$Pager',
        '__EVENTARGUMENT': 3,
        '__VIEWSTATEENCRYPTED': ''
    }
    res = requests.post(url, data=data, timeout=5)
    # res = requests.post(url,timeout=5)
    # print(res.text)
    soup = BeautifulSoup(res.text, "lxml")
    a_str = soup.find_all("td",attrs={"valign":"bottom","align":"left","nowrap":"true","width":"40%"})[0].strings
    for info in a_str:
        print(info)