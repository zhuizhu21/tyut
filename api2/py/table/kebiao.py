# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：kebiao.py
作者：刘乾 2018.10.15
功能：获取课表，返回数据给前台
参数：agrv1  cookie文件名
'''
import sys
import json
import requests
from bs4 import BeautifulSoup
from py.util import util

def remove(str1,str2):
    '''
    字符串合并
    :param str1: 
    :param str2: 
    :return: 
    '''
    if str1=='' and str2=='':
        return ''
    else:
        return (str1+str2)
def kebiao_now(filename):
    '''本学期课表'''
    res=[]
    cookie = util.load_cookie(filename)
    url="http://202.207.247.44:8089/xkAction.do?actionType=6"
    session = requests.Session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://jwc.tyut.edu.cn/",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    s = session.get(url=url, headers=headers, cookies=cookie)
    text=s.text.replace('&nbsp;\r', '-')
    text=text.replace('\r','')
    #print(text)
    #bs4 来解析网页文本
    sob = BeautifulSoup(text, "lxml")
    title=sob.find("title").get_text().strip()
    class_list=sob.find_all("tr",{"bgcolor":"#FFFFFF"})
    class_list2 = sob.find_all("tr", {"class": "odd"})
    #print(title)
    if title == "错误信息":
        return ("教务处课表查询失败")
    else:
        cou=1
        for item in class_list:
            if len(item)!=3:
                temp={}
                content = item.get_text().strip()
                content=content.replace(' ','')
                content = content.replace('午', '')
                content = content.replace('上', '')
                content = content.replace('下', '')
                content = content.replace('休', '')
                content = content.replace('晚', '')
                content = content.replace('\n', '')
                content=content.replace('--','-|')
                content=content.split('-')

                temp['Monday'] =content[2]
                temp['Tuesday'] =content[3]
                temp['Wednesday'] =content[4]
                temp['Thursday'] =content[5]
                temp['Friday'] =content[6]
                temp['Saturday'] =content[7]
                temp['Sunday'] =content[8]

                res.append(temp)
                cou=cou+1


        for item in class_list2:
            text=item.get_text().strip()
            text=text.replace(' ','')
            text = text.replace('\r', '')
            if "方案" in text:
                content=text.split()
                if len(content)>10:
                    temp={}
                    temp['id']=content[2]
                    temp['time']=content[10]
                    res.append(temp)
    return res