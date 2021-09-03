# -*- coding: utf-8 -*-
# @Time : 2021/8/27 17:28
# @Author : rational
# @File : xuanzhi_spider.py

from collections import ChainMap

import requests
from fontTools.ttLib import TTFont
from xml import etree
from bs4 import BeautifulSoup
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
}


def get_url_rsp(url):
    rsp = requests.get(url, headers=header)
    return rsp.text


def dispose_data(rsp):
    soup = BeautifulSoup(rsp, "lxml")
    # 正则匹配出字体url
    woff_url = get_font_url(rsp)
    font_map = get_font_map(woff_url)
    # print(rsp)
    find_all_list = soup.find_all("div", class_="list-item-right")
    res = []
    # print(res)
    for i in find_all_list:
        new_str_list = []
        for str_info in i.strings:
            if str_info and not str_info == "\n":
                new_str = ''.join(str_info).replace(' ', '').replace('\n', '').replace('\r', '')
                # print(''.join(str_info).replace(' ','').replace('\n',''))
                # print("_" * 100)
                new_str_list.append(new_str)
        # print(new_str_list)
        # print(new_str_list)
        res_data = {"name": new_str_list[1],
                    "place": new_str_list[-1].split("/")[1],
                    "area": 0 if len(new_str_list) == 6 else new_str_list[4],
                    "use": new_str_list[-2] if not '/' in new_str_list[-2] else new_str_list[-2].split("/")[1],
                    "time": new_str_list[-1].split("/")[0],
                    "company": new_str_list[3].split("/")[-1],
                    "status": new_str_list[3].split("/")[0],
                    "other": new_str_list[0], }
        # switch font
        if res_data.get("area"):
            new_area = []
            for i in res_data.get("area"):
                if i.isdigit() or i == ".":
                    new_area.append(i)
                else:
                    new_area.append(font_map.get("0x" + i.encode("unicode_escape")[2:].decode()).replace("*", "0"))
            res_data["area"] = "".join(new_area)
        print(res_data)
        # print("*" * 100)
        res.append(res_data)
    return res


def get_font_url(rsp):
    woff_url_regexp = re.compile("https://img2.xuanzhi.com/static/new/fonts/[a-zA-Z0-9]*/font.woff")  # regexp 表达式对象
    woff_url = woff_url_regexp.findall(rsp)[0]
    print(woff_url)
    return woff_url


def get_font_map(woff_url):
    requests.packages.urllib3.disable_warnings()
    rsp = requests.get(woff_url, headers=header, verify=False)  # 关闭https验证
    font_path = "./font.woff"
    with open("./font.woff", "wb") as code:
        code.write(rsp.content)
    font = TTFont(font_path)
    font_map = {}  # 用于存储当前页面所使用的自定义字体的映射表
    for key, value in font.getBestCmap().items():  # 使用getBestCmap方法来获取字体文件中包含的映射关系
        # 这里需要注意的是，由于getBestCmap()会将内容转化为10机制，因此在后面存入字典的时候还要转化为16进制，使用hex(), 或者使用'\u{:x}'.format(x)
        if value.startswith('0x'):  # 判断是否是uni编码
            font_map[hex(key)] = chr(int(value[3:], 16))  # 由于实习僧网页中直接使用的是字符编码，所以可以直接用chr方法显示出真实字符
        else:
            font_map[hex(key)] = value.replace("*#", "")
    return font_map


def save_res(res):
    with open("./res.json", "wb") as f:
        f.write(res)


def main(urls):
    rsp = get_url_rsp(urls)
    res = dispose_data(rsp)
    print(res)
    # save_res(res)


if __name__ == "__main__":
    url = "https://www.xuanzhi.com/zhixiashi-sh/zhaopaigua/kw%E9%9D%92%E6%B5%A6%E5%8C%BA%E9%9D%92%E6%B5%A6%E5%B7%A5%E4%B8%9A%E5%9B%AD%E5%8C%BA%E5%B4%A7%E7%85%8C%E8%B7%AF%E5%8C%97%E4%BE%A7F-18-09%E5%9C%B0%E5%9D%97"
    main(url)
