import xlwt
from xlutils.copy import copy
from xlrd import *
import re

def open_file(path):
    result = []
    semiresult = []
    f = open(path, 'rt')
    source = f.readlines()
    for line in source:
        semiresult.append(re.findall(r'\d+', line))
    for sres in semiresult:
        x = int(sres[1])
        x /= 1024
        x /= 1024
        x /= 1024
        x = str(x)[:5]
        result.append(x)

    return result

def zaebosh_xl(path):

    win = open_file('auto_chk_disksapce_WIN.txt')

    w = copy(open_workbook(path, formatting_info=True))
    w.get_sheet(0).write(7, 6, win[0] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(6, 6, win[1] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(5, 6, win[2] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(4, 6, win[3] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(3, 6, win[4] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(17, 6, win[5] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(18, 6, win[6] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))

    w.save(path)
zaebosh_xl('checklist.xls')
