# -*- coding: UTF-8 -*-
'''
项目：教务处查询
文件：get_pic.py
作者：刘乾 2018.08.02
功能：获取验证码，获取cookie存储到本地
参数：null
备注：上线需要替换测试数据
'''
import os
import sys
from . import util
from . import ocr_api
import requests
import random
import PIL
from PIL import Image
from io import BytesIO
def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
def get_yzm(filename):
    #访问图片记录生成的cookie 如果成功登录 此cookie可以换取数据
    url="http://202.207.247.44:8089/validateCodeAction.do"
    util.save_cookie(filename,url)
    cookie = util.load_cookie(filename)
    response=requests.get(url=url,cookies=cookie)
    rand=filename
    #cookie=response.cookies
    image = Image.open(BytesIO(response.content))
    im=image.convert('L')
    binaryImage = im.point(initTable(), '1')
    im1 = binaryImage.convert('L')
    im1.save("/opt/tomcat/webapps/tyut/pic/"+rand+".jpg")
    content=ocr_api.get_text("/opt/tomcat/webapps/tyut/pic/"+rand+".jpg")
    os.system("rm -rf /opt/tomcat/webapps/tyut/pic/" + rand + ".jpg")
    return content
