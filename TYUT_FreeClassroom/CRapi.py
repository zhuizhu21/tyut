import urllib.request, http.cookiejar, random, os, sys, time, requests, base64, json, threading
import pandas as pd
from PIL import Image
from io import BytesIO
from aip import AipOcr #百度人工智能平台
from bs4 import BeautifulSoup

'''
为了实现自动查询 可以使用验证码识别
爬取数据采用手动输入验证码的方式
'''

class_map = {"明向校区": {
    "807": "行远楼",
    "804": "行思楼",
    "803": "行逸楼",
    "818": "行勉楼",
    "801": "行知楼"
},
    "迎西校区": {
        "108": "思韵楼",
        "105": "逸夫楼",
        "101": "思贤楼"
    },
    "虎峪校区": {
        "201": "致明楼",
        "206": "致远楼"
    }
}

global ifb
ifb = True
# 验证码
YZM_URL = "http://202.207.247.44:8065/validateCodeAction.do"
LOGIN_URL = 'http://202.207.247.44:8065/loginAction.do'


class Yzm(object):
    '''
    处理验证码图片  上传百度文字识别平台进行图像识别
    '''

    def get_yzm(self, session):
        im = image.convert('L')
        binaryImage = im.point(self.initTable(), '1')
        im1 = binaryImage.convert('L')
        file = "".join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                      'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                                      'y', 'z'], 16))
        im1.save(os.path.dirname(os.path.realpath(__file__)) + '/img/' + file + '.png')
        with open(os.path.dirname(os.path.realpath(__file__)) + '/img/' + file + '.png', 'rb') as fp:
            os.system('rm -rf ./img/' + file + '.png')
            return self.get_text(fp.read())

    def initTable(self, threshold=140):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    def get_text(self, image):
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "false"
        options["detect_language"] = "false"
        options["probability"] = "false"
        text = client.basicGeneral(image);
        try:
            return (text['words_result'][0]['words'].replace(' ', ''))
        except:
            return "error"


def do(session, yhm, mm):
    yzm = session.get(YZM_URL).content
    image = Image.open(BytesIO(yzm))
    image.show()
    yzm_text = input('输入验证码')
    data = {'zjh': yhm, 'mm': mm, 'v_yzm': yzm_text}
    html = session.post(data=data, url=LOGIN_URL)
    sob = BeautifulSoup(html.content, 'lxml')
    info_list = sob.find_all("font", {"color": "#990000"})
    mm_error = "您的密码不正确，请您重新输入！"
    yzm_error = "你输入的验证码错误，请您重新输入！"
    yhm_error = "你输入的证件号不存在，请您重新输入！"
    sys_error = "您无法在当前时间使用本服务器登录！"
    if_bit = 1
    for info in info_list:
        content = info.get_text()
        print(content)#输出错误信息
        if content == mm_error or content == yhm_error or content == sys_error:
            global ifb
            ifb = False
            if_bit = 0
            return False
        if content == yzm_error:
            if_bit = 0
    if if_bit == 1:
        return True
    else:
        do(session=session, yhm=yhm, mm=mm)


def doGetList(yhm, mm):
    session = requests.Session()
    login_res = do(session=session, yhm=yhm, mm=mm)
    URL_GET = "http://202.207.247.44:8065/xszxcxAction.do?oper=xszxcx_lb"
    html = session.get(URL_GET)
    datas = []
    for week in range(1, 25):
        for weekend in range(1, 8):
            for classes in range(1, 12):
                datas.append([week, weekend, classes])
    # TODO:数据获取流程|DONE！
    # TODO:使用多线程并行化数据获取|DONE！
    mx_1 = threading.Thread(target=mult, args=(session, '01', '101', datas,))
    # mx_2=threading.Thread(target=mult,args=(session,'01','105',datas,))
    # mx_3 = threading.Thread(target=mult, args=(session, '01', '108', datas,))
    threads = []
    threads.append(mx_1)
    # threads.append(mx_2)
    # threads.append(mx_3)
    for t in threads:
        t.setDaemon(True)  # 将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起
        t.start()
    for t in threads:
        t.join()


# 多线程函数
def mult(session, xq, jxl, datas):
    URL = "http://202.207.247.44:8065/xszxcxAction.do?oper=tjcx"
    for ndata in datas:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/json/' + xq + '/' + jxl + '/' + str(
                ndata[0]) + '.json', 'a+') as fp:
            print('正在写入文件' + os.path.dirname(os.path.realpath(__file__)) + '/json/' + xq + '/' + jxl + '/' + str(
                ndata[0]) + '.json')
            key = str(ndata[0]) + '-' + str(ndata[1]) + '-' + str(ndata[2])
            res = []
            print(key)
            data = {
                "currentPage": "1",
                "page": "1",
                "pageNo": "",
                "pageSize:": "300",
                "zxJc": str(ndata[2]),  # 节次
                "zxJxl": jxl,
                "zxXaq": xq,
                "zxxnxq": "2018-2019-2-1",
                "zxxq": str(ndata[1]),  # 星期
                "zxZc": str(ndata[0])  # 周次
            }
            session.post(url=URL, data=data)
            detail = "http://202.207.247.44:8065/xszxcxAction.do?totalrows=300&pageSize=300"
            html = session.get(detail)
            pds = pd.read_html(html.text, attrs={"class": "displayTag"})
            for table in pds:
                for i in range(0, table.shape[0]):
                    temp = json.loads(table.loc[i].to_json(force_ascii=False))
                    temp_json = {"id": temp.get('教室'), "type": temp.get('类型'), "count": temp.get('座位数')}
                    res.append(temp_json)
            fp.write("'" + str(key) + "'" + ':' + str(res) + ',\n')


if __name__ == '__main__':
    doGetList('2015002028', '277538')
