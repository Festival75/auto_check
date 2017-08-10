import xlwt
from xlutils.copy import copy
from xlrd import *
import re
import datetime
import json


with open('config.json') as data_file:
    data = json.load(data_file)

osts = data['OST']


def open_file(ost):
    result = []
    semiresult = []
    f = open('resources/txt/' + ost + '.txt', 'rt')
    source = f.readlines()
    for line in source:
        semiresult.append(re.findall(r'\d+', line))
    for sres in semiresult:
        x = float(sres[1])
        x /= 1024
        x /= 1024
        x /= 1024
        x = str(x)[:5]
        result.append(x)
    return result


def txt_to_exel(ost, txt_to_input):
    w = copy(open_workbook(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'], formatting_info=True))
    w.get_sheet(0).write(7, 6, txt_to_input[0] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(6, 6, txt_to_input[1] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(5, 6, txt_to_input[2] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(4, 6, txt_to_input[3] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(3, 6, txt_to_input[4] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(17, 6, txt_to_input[5] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(18, 6, txt_to_input[6] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(25, 2, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), xlwt.easyxf("align: vert centre, horiz center; borders: left medium, right medium, top medium, bottom medium"))
    w.save(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'])


for ost in osts:
    txt_to_exel(ost, open_file(ost))
