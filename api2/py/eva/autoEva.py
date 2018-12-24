'''
教学评估
作者：刘乾 2018.11.20
功能：获取课表，返回数据给前台
参数：cookie文件名
'''
import sys
import json
import requests
import json
import urllib.parse
import time
from py.util import util
from bs4 import BeautifulSoup



session=requests.session()
def getEvaList(filename):
    '''获取待评估列表'''
    todoList = []
    cookie = util.load_cookie(filename)
    url="http://202.207.247.44:8089/jxpgXsAction.do?oper=listWj"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://202.207.247.44:8089/menu/s_main.jsp",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    try:

        html = session.get(url=url, headers=headers, cookies=cookie)
        bsObj = BeautifulSoup(html.text, 'lxml')
        html2list=bsObj.find_all('img',{'title':'评估'})
        count=1
        for item in html2list:
            res=item.get('name').replace('#','').split('@')
            newdic={'wjbm': res[0], 'bpr': res[1], 'pgnr': res[5],
             'oper': 'wjShow', 'wjmc': res[3], 'bprm': res[2],
             'pgnrm': res[4], 'pageSize': '20', 'page': '1', 'currentPage': '1', 'pageNo': ''}
            count+=1
            todoList.append(newdic)
    except:
        pass
    return todoList
def doEva(item):
    '''进行评估'''
    url="http://202.207.247.44:8089/jxpgXsAction.do?oper=wjpg"
    cookie = util.load_cookie(filename)

    headers = {
        "Host":"202.207.247.44:8089",
        "X-Requested-With":"cn.darkal.networkdiagnosis",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Proxy-Connection": "keep-alive",
               'Origin':'http://202.207.247.44:8089',
               "Referer": "http://202.207.247.44:8089/jxpgXsAction.do?oper=wjpg",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    string="老师的课程讲解十分细致，认真负责！"

    data={
        "wjbm":item['wjbm'],
        "bpr":item['bpr'],
        "pgnr":item['pgnr'],
        "0000000045":"10_1".encode('gbk'),
        "zgpj":string.encode('gbk'),
    }
    # data=urllib.parse.urlencode(data).encode('gbk')
    html=session.post(url=url,headers=headers,data=data,cookies=cookie)
    bsObj=BeautifulSoup(html.text,'lxml')
    res=bsObj.find_all('script')
    for item in res:
        newews=item.get_text()
        if "评估失败" in newews:
            print("评估失败")
        else:
            print("评估成功")
def dosome(filename):
    url="http://202.207.247.44:8089/jxpgXsAction.do"
    cookie = util.load_cookie(filename)
    headers = {
        "Host":"202.207.247.44:8089",
        "X-Requested-With":"cn.darkal.networkdiagnosis",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Proxy-Connection": "keep-alive",
               'Origin':'http://202.207.247.44:8089',
               "Referer": "http://202.207.247.44:8089/jxpgXsAction.do?oper=wjpg",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    todoList = getEvaList(filename)
    for item in todoList:
        html = session.post(url=url, headers=headers, data=item, cookies=cookie)
        doEva(item)
