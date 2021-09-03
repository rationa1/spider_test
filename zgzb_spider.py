# -*- coding: utf-8 -*-
# @Time : 2021/8/31 17:28
# @Author : rational
# @File : zgzb_spider.py

# https://bulletin.cebpubservice.com/

from collections import ChainMap
import requests
from fontTools.ttLib import TTFont
from xml import etree
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 注释https报错

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def get_url_rsp(url):
    rsp = requests.get(url, headers=header, verify=False)  # 取消ssl验证
    rsp.encoding = 'utf-8'  # 防止乱码
    return rsp.text


def dispose_data(rsp):
    soup = BeautifulSoup(rsp, "lxml")
    find_all_list = soup.find_all("input", attrs={"type": "radio", "name": "media"})
    # print(find_all_list)
    res = []
    for i in find_all_list:
        res.append({"url": i.get("title"),
                    "name": i.get("value")})
    return res


def main(urls):
    rsp = get_url_rsp(urls)
    # print(rsp)
    res = dispose_data(rsp)
    print(res)
    # save_res(res)


if __name__ == "__main__":
    url = "https://bulletin.cebpubservice.com/"
    main(url)
