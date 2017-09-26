import os
import json
import re
import logging
from DBcm import UseDatabaseOracle, UseDatabaseMSSQL


logging.basicConfig(filename='collect_info.log', format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)


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


def get_win_space(config: dict):
    """Обращается к виндовым серверам на основании конфигурационного файла опрашивает свободное место на дисках.
    После чего перегоняет результат в гигобайты и записывает в WinDiskSpace.json"""
    for ost in config['OST']:
        try:
            abbyy_ps_str = os.popen('winrs -r:{0} -u:{1} -p:{2} "{3}"'.format(config['ENV'][ost]['ABBYY_PS'], config['WIN_COLLECT'][ost]['USER'], config['WIN_COLLECT'][ost]['PASSWORD'], config['WIN_COLLECT'][ost]['COMMANDv1'])).read()
            abbyy_db_str = os.popen('winrs -r:{0} -u:{1} -p:{2} "{3}"'.format(config['ENV'][ost]['ABBYY_DB'], config['WIN_COLLECT'][ost]['USER'], config['WIN_COLLECT'][ost]['PASSWORD'], config['WIN_COLLECT'][ost]['COMMANDv2'])).read()
            abbyy_as_str = os.popen('winrs -r:{0} -u:{1} -p:{2} "{3}"'.format(config['ENV'][ost]['ABBYY_AS'], config['WIN_COLLECT'][ost]['USER'], config['WIN_COLLECT'][ost]['PASSWORD'], config['WIN_COLLECT'][ost]['COMMANDv2'])).read()
            icc01_str = os.popen('winrs -r:{0} -u:{1} -p:{2} "{3}"'.format(config['ENV'][ost]['ICC01'], config['WIN_COLLECT'][ost]['USER'], config['WIN_COLLECT'][ost]['PASSWORD'], config['WIN_COLLECT'][ost]['COMMANDv1'])).read()
            icc02_str = os.popen('winrs -r:{0} -u:{1} -p:{2} "{3}"'.format(config['ENV'][ost]['ICC02'], config['WIN_COLLECT'][ost]['USER'], config['WIN_COLLECT'][ost]['PASSWORD'], config['WIN_COLLECT'][ost]['COMMANDv1'])).read()
            abbyy_ps = re.findall(config['REG_EXP']['WIN_SIZE'], abbyy_ps_str)
            abbyy_db = re.findall(config['REG_EXP']['WIN_SIZE'], abbyy_db_str)
            abbyy_as = re.findall(config['REG_EXP']['WIN_SIZE'], abbyy_as_str)
            icc01 = re.findall(config['REG_EXP']['WIN_SIZE'], icc01_str)
            icc02 = re.findall(config['REG_EXP']['WIN_SIZE'], icc02_str)
            with open(config['PATH']['DISK_SPACE_FILE'] + 'WinDiskSpace.json', 'r+') as output:
                data = json.load(output)
                data[ost]['ABBYY_PS_C'] = int(float(abbyy_ps[0])//config['SIZE_TYPE'])
                data[ost]['ABBYY_DB_C'] = int(float(abbyy_db[0])//config['SIZE_TYPE'])
                data[ost]['ABBYY_DB_E'] = int(float(abbyy_db[1])//config['SIZE_TYPE'])
                data[ost]['ABBYY_AS_C'] = int(float(abbyy_as[0])//config['SIZE_TYPE'])
                data[ost]['ABBYY_AS_E'] = int(float(abbyy_as[1])//config['SIZE_TYPE'])
                data[ost]['ICC01_C'] = int(float(icc01[0])//config['SIZE_TYPE'])
                data[ost]['ICC02_C'] = int(float(icc02[0])//config['SIZE_TYPE'])
                output.seek(0)
                json.dump(data, output, indent=4)
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле win_collect: {0}'.format(str(err)))
            exit(0)


def write_sql_value_to_json(config: dict, ost: str, value: int, label: str):
    """Записать полученное значение в DBData.json, в зависимости от label"""
    try:
        with open(config['PATH']['SQL_FILE'] + 'DBData.json', 'r+') as output:
            data = json.load(output)
            if label == 'batch':
                data[ost]['ABBYYDB_BATCHPARAM'] = value
                logging.info('[+] Колличество BATCHPARAMETER для ОСТ = {0} добавленно в '.format(ost) + config['PATH']['SQL_FILE'] + 'DBData.json')
            elif label == 'queue':
                data[ost]['OSDB_QUEUEITEM'] = value
                logging.info('[+] Колличество OS1USER.QUEUEITEM для ОСТ = {0} добавленно в '.format(ost) + config['PATH']['SQL_FILE'] + 'DBData.json')
            elif label == 'conductor':
                data[ost]['OSDB_CONDUCTOR'] = value
                logging.info('[+] Колличество OS1USER.VWVQ1_CONDUCTOR для ОСТ = {0} добавленно в '.format(ost) + config['PATH']['SQL_FILE'] + 'DBData.json')
            else:
                logging.error('[-] Не распознан лейбл {0}. Пожалуйста используйте "batch" - для BATCHPARAMETER, "queue" - для OS1USER.QUEUEITEM или "conductor" - для OS1USER.VWVQ1_CONDUCTOR'.format(label))
                exit()
            output.seek(0)
            json.dump(data, output, indent=4)
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле write_sql_value_to_json: {0}'.format(str(err)))
        exit(0)


def get_batchparam(config: dict):
    """На основании строки подключения из конфига подключается к ABBYYDB и записывает колличество
    BATCHPARAMETER в DBData.json"""
    try:
        for ost in config['OST']:
            if not config['ENV'][ost]['ORACLE_CONNECT'] == "None":
                with UseDatabaseOracle(config['ENV'][ost]['ORACLE_CONNECT']) as cursor:
                    _SQL = """SELECT COUNT(bp.id) FROM BATCHPARAMETER bp"""
                    cursor.execute(_SQL)
                    batchparam = cursor.fetchall()
                write_sql_value_to_json(config, ost, int(batchparam[0][0]), 'batch')
            elif not config['ENV'][ost]['MSSQL_CONNECT'] == "None":
                with UseDatabaseMSSQL(config['ENV'][ost]['MSSQL_CONNECT']) as cursor:
                    _SQL = """SELECT COUNT(bp.id) FROM BATCHPARAMETER bp"""
                    cursor.execute(_SQL)
                    batchparam = cursor.fetchall()
                write_sql_value_to_json(config, ost, int(batchparam[0][0]), 'batch')
            else:
                logging.error('[-] Не найдена строка для подключения к Oracle/MS SQL. Проверьте config.json')
                exit()
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле get_batchparam: {0}'.format(str(err)))
        exit(0)


def get_queueitem_conductor(config: dict):
    """Получает queueitem и conductor из OSDB , вносит полученные данные в DBData.json"""
    result = []
    for ost in config['OST']:
        try:
            os.system('pscp -q sql_collect.sh root@{0}:/tmp'.format(config['ENV'][ost]['DB2']))
            output = os.popen('plink root@{0} "/usr/bin/ksh /tmp/sql_collect.sh"'.format(config['ENV'][ost]['DB2'])).read()
            logging.info('[+] Данные из OSDB {0} полученны'.format(ost))
            result.append(re.findall(r'\b\d+\b', output))
            write_sql_value_to_json(config, ost, int(result[0][0]), 'queue')
            write_sql_value_to_json(config, ost, int(result[0][1]), 'conductor')
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле get_queueitem_conductor: {0}'.format(str(err)))
            exit(0)


def main():
    config = read_config('config.json')
    get_win_space(config)
    get_batchparam(config)
    get_queueitem_conductor(config)


if __name__ == '__main__':
    main()
