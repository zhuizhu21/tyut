import requests
import datetime
import util
import time
from bs4 import BeautifulSoup
year=str(datetime.datetime.now().year)
month=str(datetime.datetime.now().month)
if  len(month)==1:
    month="0"+month
day=str(datetime.datetime.now().day)
if int(day)+1<10:
    day="0"+str(int(day)+1)
date=year+"-"+month+"-"+day
url="http://jiuye.tyut.edu.cn/zpweb/RecruitmentSpecial.aspx?Day="+date
info_url="http://jiuye.tyut.edu.cn/zpweb/"
session=requests.Session()
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "keep-alive",
           "host":"jiuye.tyut.edu.cn",
           "Referer":"http://jiuye.tyut.edu.cn/zpweb/RecruitmentSpecial.aspx?Day=2018-10-20",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
           }
print(url)
html=session.get(url=url, headers=headers).text
print('网页读取完毕')
sob=BeautifulSoup(html,'lxml')

table=sob.find_all("table",{"class":"GridViewStyle"})

table=str(table[0])
sob_2=BeautifulSoup(table,'lxml')
title_list=sob_2.find_all('td')
url_list=sob_2.find_all('a')
count=0
res_info=[]
res_url=[]
show=[]
send=""
for item in title_list:
    if '详情' not in item.get_text():
        res_info.append(item.get_text().strip().replace('\xa0',''))
for item in url_list:
    if item.get('href'):
        res_url.append(info_url+item.get('href'))
for j in range(res_url.__len__()):
    i=j*4
    temp={'name':res_info[i],'begin':res_info[i+1],'end':res_info[i+2],'place':res_info[i+3],'detail':res_url[j]}
    show.append(temp)
    temp_s="企业名称："+res_info[i]+"\n开始时间："+res_info[i+1]+"\n结束时间："+res_info[i+2]+"\n地点:"+res_info[i+3]+"\n详情："+res_url[j]
    send=send+temp_s+"\n\n"
print("正在采集数据...")
print(send)
'''
recevers_list=['1450199522@qq.com','2018508701@qq.com','1183405503@qq.com','lh847982175@qq.com','769600434@qq.com']
#recevers_list=['1450199522@qq.com']
for item in recevers_list:
    util.sendEmail(date+"太原理工大学宣讲会信息",send,item)
    time.sleep(20)
'''
