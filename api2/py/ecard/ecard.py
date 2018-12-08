# -*- coding: UTF-8 -*-
import requests
import json
import sys
import datetime

def Ecard(stucode,stupsw,daynum):
    '''
    stucode = sys.argv[1]
    stupsw = sys.argv[2]
    daynum = int(sys.argv[3])
    :param stucode: 
    :param stupsw: 
    :param daynum: 
    :return: 
    '''
    try:
        end = datetime.datetime.now()
        beg = end - datetime.timedelta(int(daynum))
        beg = datetime.datetime.strftime(beg, "%Y-%m-%d")
        end = datetime.datetime.strftime(end, "%Y-%m-%d")

        res_to_return = {}

        url = "http://202.207.245.234:9090/1001.json?stucode=" + stucode + "&stupsw=" + stupsw
        session = requests.Session()
        res = session.get(url=url)
        code = (res.json().get('resultCode'))
        url = "http://202.207.245.234:9090/0002.json?stucode=" + stucode
        res = session.get(url)
        money = res.json().get('value')[0]['balance']
        res_to_return['balance'] = money
        url = "http://202.207.245.234:9090/0005.json?stucode=" + stucode + "&startdate=" + beg + "&enddate=" + end
        res = session.get(url)
        record = res.json().get('value')
        res_to_return['record'] = record
        res_to_return['status'] = "200"
    except:
        res_to_return['status'] = "100"
    return res_to_return