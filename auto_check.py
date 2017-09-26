import datetime
import json
from openpyxl import load_workbook, drawing
import openpyxl
from openpyxl.drawing.image import Image
import logging

logging.basicConfig(filename='auto_check.log', format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)


def read_config(path_to_config: str) -> dict:
    """Считать данные из config.json"""
    try:
        with open(path_to_config) as data_file:
            data = json.load(data_file)
        logging.info('[+] Конфигурационный фаил прочитан')
        return data
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле read_config: {0}'.format(str(err)))
        exit(0)


def write_win_size(config: dict):
    """Записать данные о свободном месте на серверах Windows из WinDiskSpace.json в excel таблицу"""
    try:
        with open(config['PATH']['DISK_SPACE_FILE'] + 'WinDiskSpace.json') as wds_file:
            wds = json.load(wds_file)
        for ost in config['OST']:
            wb = load_workbook(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            w = wb.active
            w['G8'] = str(wds[ost]['ABBYY_PS_C']) + 'Gb free'
            w['G7'] = str(wds[ost]['ABBYY_DB_C']) + 'Gb free'
            w['G6'] = str(wds[ost]['ABBYY_DB_E']) + 'Gb free'
            w['G5'] = str(wds[ost]['ABBYY_AS_C']) + 'Gb free'
            w['G4'] = str(wds[ost]['ABBYY_AS_E']) + 'Gb free'
            w['G18'] = str(wds[ost]['ICC01_C']) + 'Gb free'
            w['G19'] = str(wds[ost]['ICC02_C']) + 'Gb free'
            w['C26'] = datetime.datetime.now().today()
            wb.save(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            wb.close()
            logging.info('[+] Данные о свободном месте на Windows серверах {1} записаны в {0}'.format(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'], ost))
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле write_win_size: {0}'.format(str(err)))
        exit(0)


def write_image(config: dict):
    """Записать PNG фаил из папки со скриншотами в excel таблицу"""
    for ost in config['OST']:
        try:
            wb = load_workbook(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            ws = wb.active
            img = openpyxl.drawing.image.Image(config['PATH']['VWTOOL_SCREENSHOT'] + ost + config['TYPE']['INPUT_IMAGE'])
            img.anchor(ws['U23'])
            ws.add_image(img)
            logging.info('[+] Изображение {0} записано в {1}'.format(config['PATH']['VWTOOL_SCREENSHOT'] + ost + config['TYPE']['INPUT_IMAGE'], config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL']))
            wb.save(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            wb.close()
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле write_image: {0}'.format(str(err)))
            exit(0)


def write_sql(config: dict):
    """Записать результаты SQL запросов из DBData.json в Excel таблицу"""
    try:
        with open(config['PATH']['SQL_FILE'] + 'DBData.json') as sql_file:
            sql = json.load(sql_file)
        for ost in config['OST']:
                wb = load_workbook(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
                w = wb.active
                w['G3'] = sql[ost]['ABBYYDB_BATCHPARAM']
                w['G22'] = sql[ost]['OSDB_QUEUEITEM']
                w['G24'] = sql[ost]['OSDB_CONDUCTOR']
                wb.save(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
                wb.close()
                logging.info('[+] Результаты SQL-запросов записаны в {0}'.format(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL']))
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле write_sql: {0}'.format(str(err)))
        exit(0)


def main():
    logging.info('[**] Старт программы')
    config = read_config('config.json')
    #write_image(config)
    write_win_size(config)
    write_sql(config)
    logging.info('[**] Окончание программы')


if __name__ == '__main__':
    main()
