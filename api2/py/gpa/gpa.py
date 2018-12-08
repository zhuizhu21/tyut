# -*- coding: UTF-8 -*-
from http import cookiejar
from urllib import parse
import urllib.request
import json
import sys
postUrl = "http://202.207.247.60/Hander/LoginAjax.ashx"
rankUrl = "http://202.207.247.60/Hander/Cj/CjAjax.ashx?rnd%20=%200.26650203890332436"
headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400'
}
# 获取cookie对象
cookie = cookiejar.CookieJar()
# 构建一个cookie的处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 获取一个opener对象
opener = urllib.request.build_opener(handler)


def get_gpa(username, pwd):
    data1 = {
        'u': username,
        'p': pwd,
        'r': 'on'
    }
    data1 = parse.urlencode(data1).encode('utf-8')
    # 转成url编码

    # 获取一个请求对象
    req = urllib.request.Request(postUrl, data1)
    # 请求服务器，返回响应对象，这时cookie已经随着resp对象携带过来了
    resp = opener.open(req)
    result = json.loads(resp.read().decode('utf-8'))
    if result['Code'] == 0:
        newresult = {'Code': 0, 'Msg': "用户名或密码错误！"}
        print("用户名或密码错误！")
    elif result['Code'] == 1:
        # newresult = {'Code': 0, 'Msg': "登陆成功"}
        data2 = {
            'limit': '40',
            'offset': '0',
            'order': 'asc',
            'sort': 'jqzypm,xh',
            'do': 'xsgrcj',
            'xh': username
        }

        data2 = parse.urlencode(data2).encode('utf-8')
        req2 = urllib.request.Request(rankUrl, data2)
        resp2 = opener.open(req2)
        dict1 = json.loads(resp2.read().decode('utf-8'))[0]

        claNum = "/" + dict1['bjrs']
        majorNum = "/" + dict1['zyrs']
        mainClaNum = "/" + dict1['dlrs']

        dict1['gpabjpm']=dict1['gpabjpm'] + claNum
        dict1['gpazypm']=dict1['gpazypm'] + majorNum
        dict1['gpadlpm']=dict1['gpadlpm'] + mainClaNum
        dict1['pjcjbjpm'] =dict1['pjcjbjpm'] + claNum
        dict1['pjcjzypm']=dict1['pjcjzypm'] + majorNum
        dict1['jqbjpm']=dict1['jqbjpm'] + claNum
        dict1['jqzypm']=dict1['jqzypm'] + majorNum
        return dict1
