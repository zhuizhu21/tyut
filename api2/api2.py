import random
from flask import Flask,request,Response
from py.login.login import login
from py.score.score import chengji_all
from py.gpa.gpa import get_gpa
from py.table.kebiao import kebiao_now
from py.notice.notice import notice
from py.ecard.ecard import Ecard
from py.eva.getList import getEvaList
from py.eva.autoEva import dosome

app=Flask(__name__)

@app.route('/api2/Login',methods=['GET'])
def do_login():
    '''
    登录授权接口
    :return: 参见接口文档
    '''
    yhm=request.args.get('yhm')
    mm=request.args.get('mm')
    token=get_random()
    msg=login(yhm, mm, token)
    print(msg)
    if msg==None:
        msg="200"
    res={"status":msg,"filename":token}
    return str(res)

@app.route('/api2/Score',methods=['GET'])
def get_score():
    '''
    成绩查询接口
    :return: 参见接口文档
    '''
    token=request.args.get('filename')
    res=chengji_all(token)
    return str(res)

@app.route('/api2/GPA',methods=['GET'])
def get_gpa():
    '''
    GPA接口
    :return:参见接口文档 
    '''
    yhm=request.args.get('yhm')
    mm=request.args.get('mm')
    res=get_gpa(yhm,mm)
    return str(res)

@app.route('/api2/Table',methods=['GET'])
def get_table():
    token=request.args.get('filename')
    res=kebiao_now(token)
    return str(res)

@app.route('/api2/Notice',methods=['GET'])
def get_notice():
    res=notice()
    return str(res)

@app.route('/api2/Ecard',methods=['GET'])
def get_ecard():
    yhm=request.args.get('yhm')
    mm=request.args.get('mm')
    date=request.args.get('date')
    res=Ecard(yhm,mm,date)
    return str(res)

@app.route('/api2/GetList',methods=['GET'])
def get_list():
    token=request.args.get('filename')
    res=getEvaList(token)
    return str(res)

@app.route('/api2/AutoEva',methods=['GET'])
def auto_eva():
    token=request.args.get('filename')
    res=dosome(token)
    return str(res)



def get_random():
    ori = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z'
        ,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
        , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    res=""
    for i in range(32):
        res+=ori[random.randint(0,61)]
    return res

if __name__=="__main__":
    app.run()
