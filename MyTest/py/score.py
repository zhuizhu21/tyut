# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：score.py
作者：刘乾 2018.08.02
功能：获取课表，返回数据给前台
参数：agrv1  cookie文件名
备注：上线需要替换测试数据
'''
import sys
from . import util
import requests
from bs4 import BeautifulSoup
def chengji_all(filename):
    '''全部及格成绩'''
    res = []
    cookie=util.load_cookie(filename)
    url = "http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2017-2018学年春(两学期)#qb_2017-2018学年春(两学期)"
    # url='http://202.207.247.44:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=5585'
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
        #print("**********及格成绩**********")
        sob = BeautifulSoup(s.content, "lxml")
        list = sob.find_all("td", {"align": "center"})
        value_list = []
        for value in list:
            value_t = value.get_text().strip()
            if len(value_t) != 0:
                # print(value_t)
                value_list.append(value_t)
        cou = 0
        value_list.reverse()
        #{"score":"88.0","attri":"专业选修","gp":"2","name":"物联网传输课程设计"}
        score=""
        attri=""
        gp=""
        name=""
        temp={}

        for info in value_list:
            cou = cou + 1
            if cou == 1:#成绩
                temp['score']=info.strip()
            if cou == 2:#属性
                temp['attri']=info.strip()
            if cou == 3:#学分
                temp['gp']=info.strip()
            if cou == 5:#名称
                temp['name']=info.strip()
            if cou==7:
                cou=0
                res.append(temp)
                temp={}
    else:
        print("登录失败请刷新重试")
    return res
