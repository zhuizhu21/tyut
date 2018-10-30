# -*- coding: UTF-8 -*-
from django.http import HttpResponse as response
from .get_name import get_random
from .py import login
from .py import score
from .py import gpa
from .py import kebiao
from .py import notice
import json
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