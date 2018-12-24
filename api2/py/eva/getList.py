'''
教学评估
文件：kebiao.py
作者：刘乾 2018.11.20
功能：获取课表，返回数据给前台
参数：cookie文件名
'''
import sys
import json
import requests
from bs4 import BeautifulSoup
from py.util import util




def getEvaList(filename):
    '''获取待评估列表'''
    toShow=[]
    cookie = util.load_cookie(filename)
    url="http://202.207.247.44:8089/jxpgXsAction.do?oper=listWj"
    session = requests.Session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Connection": "keep-alive",
               "Referer": "http://202.207.247.44:8089/menu/s_main.jsp",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
               }
    try:

        html = session.get(url=url, headers=headers, cookies=cookie)
        # print(html.text)
        bsObj = BeautifulSoup(html.text, 'lxml')
        html2list=bsObj.find_all('img',{'title':'评估'})
        count=1
        for item in html2list:
            res=item.get('name').replace('#','').split('@')
            newdic={'wjbm': res[0], 'bpr': res[1], 'pgnr': res[5],
             'oper': 'wjShow', 'wjmc': res[3], 'bprm': res[2],
             'pgnrm': res[4]}
            count+=1
            toShow.append(newdic)
    except:
        pass
    return {"size":len(toShow),"content":toShow}
