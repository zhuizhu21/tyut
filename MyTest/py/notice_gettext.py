# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：notice.py
作者：刘乾 2018.09.02
功能：获取教务处通知 返回给前台
参数：url
'''
import sys
import requests
from bs4 import BeautifulSoup

def get_text(url):
    '''教务处通知'''
    #url=sys.argv[1]
    session = requests.Session()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "jwc.tyut.edu.cn",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }
    s = session.get(url=url, headers=headers)
    text=s.content.decode('utf-8')
    text=text.replace('\r','')
    #print(text)
    sob=BeautifulSoup(s.content,'lxml')
    content=sob.find_all("p")
    toshow=""
    for item in content:
        toshow+=item.get_text().strip()
        #print(item.get_text().strip())
    toshow=toshow.replace('版权所有：太原理工大学教务处','')
    toshow=toshow.replace('地址：山西省太原市迎泽西大街79号 | 邮政编码：030024 | 电话：0351-6010300','')
    return toshow