# Иморт необходимых библиотек
import xlwt
from xlutils.copy import copy
from xlrd import *
import re


# Функция получает на вход путь к файлу и парсит его
def open_file(path):
    # Создаём два пустых листа для хранения данных парсинга
    result = []
    semiresult = []
    # Открываем фаил в режиме чтения текста
    f = open(path, 'rt')
    # Считываем строки из файла в лист
    source = f.readlines()
    # Пока есть строки в листе
    for line in source:
        # Добавляем к промежуточному листу отформатированную строку
        semiresult.append(re.findall(r'\d+', line))
    # Пока есть строки в промежуточном листе
    for sres in semiresult:
        # Переводим байты в Гигабайты
        x = float(sres[1])
        x /= 1024
        x /= 1024
        x /= 1024
        # Устанавливаем точность 2 знака после запятой
        x = str(x)[:5]
        # Добавляем полученное число к финальному листу
        result.append(x)
    # Возвращаем финальный лист с размером в гигабайтах
    return result


def txt_to_exel(path, ost):
    w = copy(open_workbook(path, formatting_info=True))
    w.get_sheet(0).write(7, 6, ost[0] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(6, 6, ost[1] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(5, 6, ost[2] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(4, 6, ost[3] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(3, 6, ost[4] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(17, 6, ost[5] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.get_sheet(0).write(18, 6, ost[6] + 'Gb free', xlwt.easyxf("align: vert centre, horiz center"))
    w.save(path)


# Функция преднозначена для внесения значений в exel-таблицу
def zaebosh_xl(path, ost):
    if ost == 'TNO':
        txt = open_file('TNO.txt')
        txt_to_exel(path, txt)
    elif ost == 'TMN':
        txt = open_file('TMN.txt')
        txt_to_exel(path, txt)


zaebosh_xl('checklist_TNO.xls', 'TNO')
zaebosh_xl('checklist_TMN.xls', 'TMN')
