# -*- coding: UTF-8 -*-
'''
登录
'''
import os
import sys
import requests
import random
import time
from py.util import util
from py.util import ocr_api
from py.util import get_pic
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


def login(yhm,mm,filename):
    '''登录'''
    yzm = get_pic.get_yzm(filename)
    while yzm=="error":
        time.sleep(0.2)
        yzm=get_pic.get_yzm(filename)
    cookie=util.load_cookie(filename)
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
            if_bit = 2
            return str(mm_error)
        elif info.get_text() == yzm_error:
            if_bit = 0
        else :
            if_bit = 2
            return str(yhm_error)
    if if_bit==1:
        return str(200)
    else:
        time.sleep(0.5)
        login(yhm, mm, filename)