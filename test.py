import requests
import random
import os
import sys
import time
import pytesseract
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
#全局变量部分
global cookie
global yzm
#函数部分
def get_yzm():
    #访问图片记录生成的cookie 如果成功登录 此cookie可以换取数据
    url="http://202.207.247.44:8089/validateCodeAction.do"
    response=requests.get(url)
    global cookie
    rand=str(int(random.random()*10000))
    cookie=response.cookies
    image = Image.open(BytesIO(response.content))
    image.save("/home/pic/"+rand+".jpg")
    im = Image.open("/home/pic/"+rand+".jpg")

    imgry = im.convert('L')
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    out.save("/home/pic/"+rand+".jpg")
    im = Image.open("/home/pic/" + rand + ".jpg")

    data=im.getdata()
    w,h =im.size
    black_point=0
    for x in range(1,w-1):
        for y in range(1,h-1):
            mid_piexl=data[w*y+x]#中央像素点像素值
            if mid_piexl < 140:
                top_piexl=data[w*(y-1)+x]
                left_piexl=data[w*y+(x-1)]
                down_piexl=data[w*(y+1)+x]
                right_piexl=data[w*y+(x+1)]
                if top_piexl < 5:
                    black_point += 1
                if left_piexl < 5:
                    black_point += 1
                if down_piexl < 5:
                    black_point += 1
                if right_piexl < 5:
                    black_point += 1
                if black_point < 1:
                    im.putpixel((x, y), 255)
                black_point = 0
    im.save("/home/pic/"+rand+".jpg")
    out=Image.open("/home/pic/"+rand+".jpg")
    yzm=pytesseract.image_to_string(out)
    yzm=yzm.replace(' ','')
    os.system("rm -rf /home/pic/"+rand+".jpg")
    return yzm




def login():
    '''登录'''
    yhm=sys.argv[1]
    mm=sys.argv[2]
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


def xueji_info():
    '''学籍信息'''
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
        # print(s.text)
        print("**********学籍信息**********")
        list = sob.find_all("td", {"class": "fieldName"})
        '''for key in list:
            key_t=key.get_text().strip()
            print(key_t)
        '''
        list2 = sob.find_all("td", {"align": "left"})
        value_list = []
        for value in list2:
            value_t = value.get_text().strip()
            if len(value_t) != 0:
                # print(value_t)
                value_list.append(value_t)
        for info in value_list:
            print(info)
        print("*******************************")
    else:
        print("学籍信息获取失败")
def kebiao_now():
    '''本学期课表'''
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
    print(s.text)


def chengji_all():
    '''全部及格成绩'''

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
        print("**********及格成绩**********")
        sob = BeautifulSoup(s.content, "lxml")
        list = sob.find_all("td", {"align": "center"})
        value_list = []
        for value in list:
            value_t = value.get_text().strip()
            if len(value_t) != 0:
                # print(value_t)
                value_list.append(value_t)
        cou = 0
        for info in value_list:
            cou = cou + 1
            if cou == 3:
                print(info)
            if cou == 7:
                print(info)
                cou = 0
                # print(s.text)
        xueji_info()
        #kebiao_now()
    else:
        print("登录失败请刷新重试")

yzm=get_yzm()
login()
chengji_all()