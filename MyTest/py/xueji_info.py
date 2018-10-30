# -*- coding: UTF-8 -*-
import sys
import util
import requests
from bs4 import BeautifulSoup
global filename
filename=sys.argv[1]
def xueji_info():
    '''学籍信息'''
    cookie=util.load_cookie(filename)
    url = 'http://202.207.247.44:8089/xjInfoAction.do?oper=xjxx'
    session = requests.Session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://jwc.tyut.edu.cn/",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    s = session.get(url=url, headers=headers, cookies=cookie)
    if s.status_code == 200:
        sob = BeautifulSoup(s.content, "lxml")
        #print(s.text)
        #list key列表 项目名称 list2 value列表 项目数据
        list = sob.find_all("td", {"width": "180"})
        key_list=[]
        for key in list:
            key_t=key.get_text().strip()
            key_list.append(key_t)
        list2 = sob.find_all("td", {"width":"275"})
        value_list = []
        for value in list2:
            value_t = value.get_text().strip()
            value_list.append(value_t)
        '''
                for key in key_list:
            print(key)
        for info in value_list:
            print(info)
        '''
        for i in range(len(key_list)):
            print(key_list[i])
            print(value_list[i])
    else:
        print("学籍信息获取失败")
xueji_info()