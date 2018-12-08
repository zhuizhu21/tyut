# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：notice.py
作者：刘乾 2018.08.02
功能：获取教务处通知 返回给前台
参数：无
'''
import requests
from . import notice_gettext
from bs4 import BeautifulSoup

def notice():
    res=[]
    '''教务处通知'''
    urlall="http://jwc.tyut.edu.cn/"
    url="http://jwc.tyut.edu.cn/tzgg.htm"
    session = requests.Session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://jwc.tyut.edu.cn/",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    s = session.get(url=url, headers=headers)
    sob=BeautifulSoup(s.content,'lxml')
    title_list_sob=sob.find_all("span",{"class":"n","style":"FLOAT: left"})
    data_list_sob = sob.find_all("span", {"class": "n", "style": "FLOAT: right"})
    title_list=[]
    data_list=[]
    url_list = []
    for title in title_list_sob:#构造标题列表
        title_list.append(title.get_text())
    for data in data_list_sob:#构造日期列表
        data_list.append(data.get_text())
    for item in title_list_sob:#构造url列表
        url_list_sob=item.find_all('a')
        for url_temp in url_list_sob:
            url_list.append(url_temp.get('href'))
    for i in range(len(title_list)):
        #{“title”:””,”content”:””,”date”:””}
        temp={}
        url_totext=urlall+url_list[i]
        temp['title']=title_list[i]
        temp['content']=notice_gettext.get_text(url_totext)
        temp['date']=data_list[i]
        res.append(temp)
    return res