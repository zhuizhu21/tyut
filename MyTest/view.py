# -*- coding: UTF-8 -*-
from django.http import HttpResponse as response
from .py import login
from .py import score
from .py import gpa
from .py import kebiao
from .py import notice
import random
import json

def get_random():
    ori = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z'
        ,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
        , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    res=""
    for i in range(32):
        res+=ori[random.randint(0,61)]
    return res

def Login(request):
    yhm=request.GET['yhm']
    mm=request.GET['mm']
    if yhm =="" or mm=="":
        return response("error")
    filename=get_random()
    status=login.login(yhm=yhm,mm=mm,filename=filename)
    temp={"status":status,"filename":filename}
    res=json.dumps(temp)
    return response(res)
def Score(request):
    filename=request.GET['filename']
    if filename=="":
        return response("error")
    temp=score.chengji_all(filename=filename)
    res=json.dumps(temp,ensure_ascii=False)
    return response(res)
def GPA(request):
    yhm=request.GET['yhm']
    mm=request.GET['mm']
    if yhm =="" or mm=="":
        return response("error")
    temp=gpa.login(username=yhm,pwd=mm)
    res = json.dumps(temp, ensure_ascii=False)
    return response(res)
def Table(request):
    filename = request.GET['filename']
    if filename=="":
        return response("error")
    temp=kebiao.kebiao_now(filename)
    res = json.dumps(temp, ensure_ascii=False)
    return response(res)
def Notice(request):
    temp=notice.notice()
    res = json.dumps(temp, ensure_ascii=False)
    return response(res)