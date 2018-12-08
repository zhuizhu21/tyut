# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：login.py
作者：刘乾 2018.08.02
功能：获取用户名和密码，获取验证码提供给前台，获取登录成功的cookie存储到本地
参数：agrv1 用户名 argv2 密码  argv3  cookie文件名
备注：上线需要替换测试数据
'''
import os
import sys
from . import util
import requests
import random
from . import ocr_api
from . import get_pic
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


def login(yhm,mm,filename):
    '''登录'''
    yzm = get_pic.get_yzm(filename)
    while yzm=="error":
        yzm=get_pic.get_yzm(filename)
    cookie=util.load_cookie(filename)
    #yhm=sys.argv[1]
    #mm=sys.argv[2]
    url = 'http://202.207.247.44:8089/loginAction.do'
    params = {'zjh': yhm, 'mm': mm, 'v_yzm': yzm}
    session = requests.Session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://jwc.tyut.edu.cn/",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    s = session.post(url=url, data=params, headers=headers, cookies=cookie)
    sob=BeautifulSoup(s.content,'lxml')
    info_list=sob.find_all("font",{"color":"#990000"})
    mm_error="您的密码不正确，请您重新输入！"
    yzm_error="你输入的验证码错误，请您重新输入！"
    yhm_error="你输入的证件号不存在，请您重新输入！"
    if_bit=1
    for info in info_list:
        if info.get_text() == mm_error:
            return (mm_error)
            if_bit=2
        elif info.get_text() == yzm_error:
            #print(yzm_error)
            if_bit = 0
        else :
            return (yhm_error)
            if_bit=2
    if if_bit==1:
        return ("200")
    elif if_bit==0:
        login(yhm,mm,filename)
    else:
        pass