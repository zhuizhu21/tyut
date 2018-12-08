# -*- coding: UTF-8 -*-
'''
说明：工具类
功能：加载cookie 保存cookie
'''
import urllib.request
import http.cookiejar
path="/media/sh/软件/code/flask/api2/py/util/cookies/"
def save_cookie(filename,url):
    cookie_file =path+filename+".txt"
    cookie = http.cookiejar.MozillaCookieJar(cookie_file)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url,headers={"Connection": "keep-alive"})
    response = opener.open(request)
    cookie.save(ignore_discard=True, ignore_expires=True)

def load_cookie(filename):
    cookie_file = path+filename+".txt"
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
    return cookie