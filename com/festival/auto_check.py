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

    x = open_file('diskspace.txt')

    w = copy(open_workbook(path, formatting_info=True))
    w.get_sheet(0).write(7, 6, x[0] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(6, 6, x[1] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(5, 6, x[2] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(4, 6, x[3] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(3, 6, x[4] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(17, 6, x[5] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(18, 6, x[6] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))

    w.save(path)
zaebosh_xl('checklist_TNO_050517.xls')
