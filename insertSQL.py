import json
import xlwt
from xlutils.copy import copy
from xlrd import *
import datetime

with open('config.json') as data_file:
    data = json.load(data_file)

with open('resources/sql/DBData.json') as sql_file:
    sql = json.load(sql_file)

osts = data['OST']


def sql_to_xl(ost):
    w = copy(open_workbook(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'], formatting_info=True))
    w.get_sheet(0).write(2, 6, sql[ost]['QUEUEITEM'], xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(21, 6, sql[ost]['BATCHPARAM'], xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(24, 6, sql[ost]['CONDUCTOR'], xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(25, 2, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), xlwt.easyxf(
        "align: vert centre, horiz center; borders: left medium, right medium, top medium, bottom medium"))
    w.save(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'])


for ost in osts:
    sql_to_xl(ost)
