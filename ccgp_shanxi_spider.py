# -*- coding: utf-8 -*-
# @Time : 2021/9/1 14:38
# @Author : rational
# @File : ccgp_shanxi_spider.py

import requests
import json

url = 'http://www.ccgp-shanxi.gov.cn/front/search/category'
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "64",
    "Content-Type": "application/json",
    "Host": "www.ccgp-shanxi.gov.cn",
    "Origin": "http://www.ccgp-shanxi.gov.cn",
    "Referer": "http://www.ccgp-shanxi.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/index.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def get_post_data():
    data = {
        'categoryCode': "ZcyAnnouncement1",
        'pageNo': "1",
        'pageSize': "100"
    }
    return data


def get_response(url):
    res = []
    data = get_post_data()
    response = requests.post(url, headers=headers, json=data)
    res.append(response.json())
    print(response.json())
    for i in range(response.json().get("hits", {}).get("total", 0) / data['pageSize']):
        data['pageNo'] += 1
        response = requests.post(url, headers=headers, json=data)
        res.append(response.json())
    return res


def dispose_response_data(rsp):
    res = []
    if isinstance(rsp, list):
        for data in rsp:
            disponse_data(res, data)
    else:
        disponse_data(res, rsp)
    return res


def disponse_data(res, data):
    pass


def main():
    rsp_text = get_response(url)
    dispose_response_data(rsp_text)


if __name__ == '__main__':
    main()
