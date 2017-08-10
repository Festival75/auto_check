from PIL import Image
from xlutils.copy import copy
from xlrd import *
import json


with open('config.json') as data_file:
    data = json.load(data_file)

osts = data['OST']


def png_to_bmp(ost):
    try:
        Image.open(data['PATH']['VWTOOL_SCREENSHOT'] + ost + data['TYPE']['VWTOOL_SCREENSHOT']).convert("RGB").save(data['PATH']['VWTOOL_SCREENSHOT'] + ost + data['TYPE']['INPUT_IMAGE'])
    except FileNotFoundError as err:
        try:
            Image.open(data['PATH']['VWTOOL_SCREENSHOT'] + ost + data['TYPE']['VWTOOL_SCREENSHOT_ALT']).convert("RGB").save(data['PATH']['VWTOOL_SCREENSHOT'] + ost + data['TYPE']['INPUT_IMAGE'])
        except FileNotFoundError:
            print('No such file ' + ost + '.PNG/.png')


def bmp_to_xls(ost):
    w = copy(open_workbook(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'], formatting_info=True))
    sheet = w.get_sheet(0)
    sheet.insert_bitmap(data['PATH']['VWTOOL_SCREENSHOT'] + ost + data['TYPE']['INPUT_IMAGE'], 23, 6)
    w.save(data['PATH']['XLS_FILE'] + ost + data['TYPE']['EXEL'])


for ost in osts:
    png_to_bmp(ost)
    bmp_to_xls(ost)
