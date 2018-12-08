# -*- coding: UTF-8 -*-

from PIL import Image
from io import BytesIO
from aip import AipOcr

APP_ID = '11728551'
API_KEY = 'oMrNBzaYpv06GOmGrE90kB1o'
SECRET_KEY = 'cAPvZE55nzgEOMkmpGoUw0MCnVXOHNgx'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """
def get_file_content(path):
    with open(path, 'rb') as fp:
        return fp.read()


def get_text(path):
    image = get_file_content(path)
    """ 调用通用文字识别, 图片参数为本地图片 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "false"
    options["detect_language"] = "false"
    options["probability"] = "false"
    text=client.basicGeneral(image);
    try:
        return (text['words_result'][0]['words'].replace(' ',''))
    except:
        return "error"