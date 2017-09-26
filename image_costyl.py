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


def write_image(config: dict):
    """Записать PNG фаил из папки со скриншотами в excel таблицу"""
    for ost in config['OST']:
        try:
            wb = load_workbook(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            ws = wb.active
            img = openpyxl.drawing.image.Image(
                config['PATH']['VWTOOL_SCREENSHOT'] + ost + config['TYPE']['INPUT_IMAGE'])
            img.anchor(ws.cell(row=25, column=22))
            ws.add_image(img)
            logging.info('[+] Изображение {0} записано в {1}'.format(
                config['PATH']['VWTOOL_SCREENSHOT'] + ost + config['TYPE']['INPUT_IMAGE'],
                config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL']))
            wb.save(config['PATH']['XLS_FILE'] + ost + config['TYPE']['EXCEL'])
            wb.close()
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле write_image: {0}'.format(str(err)))
            exit(0)


def main():
    config = read_config('config.json')
    write_image(config)


if __name__ == '__main__':
    main()
