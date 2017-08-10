import json
import xlwt
from xlutils.copy import copy
from xlrd import *
import datetime
import pprint

with open('config.json') as data_file:
    data = json.load(data_file)

osts = data['OST']
print(osts)