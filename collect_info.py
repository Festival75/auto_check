import os
import json
import re
import logging
from DBcm import UseDatabaseOracle, UseDatabaseMSSQL

logging.basicConfig(filename='collect.log', format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)


def read_config(path_to_config: str) -> dict:
    """Считать данные из config.json"""
    try:
        with open(path_to_config) as data_file:
            data = json.load(data_file)
        print('[+] Reading config file')
        logging.info('[+] Конфигурационный фаил прочитан')
        return data
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле read_config: {0}'.format(str(err)))
        exit(0)


def get_win_space(config: dict):
    """Обращается к виндовым серверам на основании конфигурационного файла опрашивает свободное место на дисках.
    После чего перегоняет результат в гигобайты и записывает в WinDiskSpace.json"""
    for ost in config['OST']:
        abps = config['ENV'][ost]['ABBYY_PS']
        abdb = config['ENV'][ost]['ABBYY_DB']
        abas = config['ENV'][ost]['ABBYY_AS']
        icc1 = config['ENV'][ost]['ICC01']
        icc2 = config['ENV'][ost]['ICC02']
        user = config['ENV'][ost]['USER']
        pwrd = config['ENV'][ost]['PASSWORD']
        cmd1 = config['ENV'][ost]['COMMANDv1']
        cmd2 = config['ENV'][ost]['COMMANDv2']
        c1ru = 'winrs -r:{0} -u:{1} -p:{2} "dir c:\ /-C |find "свободно""'
        c2ru = 'winrs -r:{0} -u:{1} -p:{2} "dir c:\ e:\ /-C |find "свободно""'
        cmen = 'winrs -r:{0} -u:{1} -p:{2} "{3}"'
        rews = config['REG_EXP']['WIN_SIZE']
        outp = config['PATH']['DISK_SPACE_FILE'] + 'WinDiskSpace.json'
        try:
            if ost == 'SPB':
                abbyy_ps = re.findall(rews, os.popen(c1ru.format(abps, user, pwrd)).read())
                abbyy_db = re.findall(rews, os.popen(c2ru.format(abdb, user, pwrd)).read())
                abbyy_as = re.findall(rews, os.popen(c2ru.format(abas, user, pwrd)).read())
                icc01 = re.findall(rews, os.popen(c1ru.format(icc1, user, pwrd)).read())
                icc02 = re.findall(rews, os.popen(c1ru.format(icc2, user, pwrd)).read())
            else:
                abbyy_ps = re.findall(rews, os.popen(cmen.format(abps, user, pwrd, cmd1)).read())
                abbyy_db = re.findall(rews, os.popen(cmen.format(abdb, user, pwrd, cmd2)).read())
                abbyy_as = re.findall(rews, os.popen(cmen.format(abas, user, pwrd, cmd2)).read())
                # Уфимский костыль, необходим при запуске локально с первого ИЦЦ ТУР
                if icc1 == "vus01-icc01-01.ufa.tn.corp":
                    icc01 = re.findall(rews, os.popen(cmd1).read())
                else:
                    icc01 = re.findall(rews, os.popen(cmen.format(icc1, user, pwrd, cmd1)).read())
                # Конец Уфимского костыля
                icc02 = re.findall(rews, os.popen(cmen.format(icc2, user, pwrd, cmd1)).read())
            print('[+] WinSize {0} info collected:'.format(ost))
            print('    {0} abbyy_ps: {1}'.format(ost, abbyy_ps))
            print('    {0} abbyy_db: {1}'.format(ost, abbyy_db))
            print('    {0} abbyy_as: {1}'.format(ost, abbyy_as))
            print('    {0} icc01: {1}'.format(ost, icc01))
            print('    {0} icc01: {1}'.format(ost, icc02))
            logging.info('[+] Информация о свободном месте на Windows серверах {0} собрана'.format(ost))
            abbyy_ps_c = int(float(abbyy_ps[0]) // 1073741824)
            abbyy_db_c = int(float(abbyy_db[0]) // 1073741824)
            abbyy_db_e = int(float(abbyy_db[1]) // 1073741824)
            abbyy_as_c = int(float(abbyy_as[0]) // 1073741824)
            abbyy_as_e = int(float(abbyy_as[1]) // 1073741824)
            icc01_c = int(float(icc01[0]) // 1073741824)
            icc02_c = int(float(icc02[0]) // 1073741824)

            with open(outp, 'r+') as output:
                data = json.load(output)
                data[ost]['ABBYY_PS_C'] = abbyy_ps_c
                data[ost]['ABBYY_DB_C'] = abbyy_db_c
                data[ost]['ABBYY_DB_E'] = abbyy_db_e
                data[ost]['ABBYY_AS_C'] = abbyy_as_c
                data[ost]['ABBYY_AS_E'] = abbyy_as_e
                data[ost]['ICC01_C'] = icc01_c
                data[ost]['ICC02_C'] = icc02_c
                output.seek(0)
                json.dump(data, output, indent=4)
            print('[+] WinSize {0} written into json {1}:'.format(ost, outp))
            print('    {0} abbyy_ps_c: {1} Gb free'.format(ost, abbyy_ps_c))
            print('    {0} abbyy_db_c: {1} Gb free'.format(ost, abbyy_db_c))
            print('    {0} abbyy_db_e: {1} Gb free'.format(ost, abbyy_db_e))
            print('    {0} abbyy_as_c: {1} Gb free'.format(ost, abbyy_as_c))
            print('    {0} abbyy_as_e: {1} Gb free'.format(ost, abbyy_as_e))
            print('    {0} icc01_c: {1} Gb free'.format(ost, icc01_c))
            print('    {0} icc01_c: {1} Gb free'.format(ost, icc02_c))
            logging.info('[+] Информация о свободном месте Windows серверов {0} записана в json {1}'.format(ost, outp))
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле get_win_space: {0}'.format(str(err)))
            exit(0)


def get_aix_space(config: dict):
    """Собирате информацию о всех разделах AIX сервера, занятых более чем на 79%"""
    try:
        aixp = config['PATH']['AIX_COLLECT']
        for ost in config['OST']:
            hosts = config['ENV'][ost]['AIX_HOSTS']
            for host in hosts:
                os.system('pscp -q {0} root@{1}:/tmp'.format(aixp, host))
                output = os.popen('plink root@{0} "/usr/bin/ksh /tmp/{1}'.format(host, aixp))
                print(host)
                print(output)
            print('[+] AIX_Space {0} collected'.format(ost))
            logging.info('[+] Информация о разделах серверов AIX {0} собрана'.format(ost))
    except Exception as err:
        logging.error('[-] Произошла ошибка в модуле get_aix_space: {0}'.format(str(err)))
        exit(0)


def write_sql_value_to_json(config: dict, ost: str, value: int, label: str):
    """Записать полученное значение в DBData.json, в зависимости от label"""
    try:
        outp = config['PATH']['SQL_FILE'] + 'DBData.json'
        with open(outp, 'r+') as output:
            data = json.load(output)
            if label == 'batch':
                data[ost]['ABBYYDB_BATCHPARAM'] = value
                print('[+] BatchParameters {0} written into json {1}'.format(ost, outp))
                logging.info('[+] BatchParameters {0} записаны в {1} '.format(ost, outp))
            elif label == 'queue':
                data[ost]['OSDB_QUEUEITEM'] = value
                print('[+] OSDB_QUEUEITEM {0} written into json {1}'.format(ost, outp))
                logging.info('[+] OSDB_QUEUEITEM {0} записаны в {1} '.format(ost, outp))
            elif label == 'conductor':
                data[ost]['OSDB_CONDUCTOR'] = value
                print('[+] OSDB_CONDUCTOR {0} written into json {1}'.format(ost, outp))
                logging.info('[+] OSDB_CONDUCTOR {0} записаны в {1} '.format(ost, outp))
            else:
                logging.error('[-] Не распознан лейбл {0}'.format(label))
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
            _SQL = config['SQL']['BP']
            cora = config['ENV'][ost]['ORACLE_CONNECT']
            cmsq = config['ENV'][ost]['ORACLE_CONNECT']
            if not cora == "None":
                with UseDatabaseOracle(cora) as cursor:
                    cursor.execute(_SQL)
                    bp = cursor.fetchall()
                print('[+] AbbyyDB data {0} collected'.format(ost))
                logging.info('[+] Данные из AbbyyDB {0} получены'.format(ost))
                write_sql_value_to_json(config, ost, int(bp[0][0]), 'batch')
            elif not cmsq == "None":
                with UseDatabaseMSSQL(cmsq) as cursor:
                    cursor.execute(_SQL)
                    bp = cursor.fetchall()
                print('[+] AbbyyDB data {0} collected'.format(ost))
                logging.info('[+] Данные из AbbyyDB {0} получены'.format(ost))
                write_sql_value_to_json(config, ost, int(bp[0][0]), 'batch')
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
        db2 = config['ENV'][ost]['DB2']
        fname = config['PATH']['SQL_COLLECT']
        reos = config['REG_EXP']['OSDB']
        try:
            os.system('pscp -q {0} root@{1}:/tmp'.format(fname, db2))
            output = os.popen('plink root@{0} "/usr/bin/ksh /tmp/{1}"'.format(db2, fname)).read()
            print('[+] OSDB data {0} collected'.format(ost))
            logging.info('[+] Данные из OSDB {0} получены'.format(ost))
            result.append(re.findall(reos, output))
            write_sql_value_to_json(config, ost, int(result[0][0]), 'queue')
            write_sql_value_to_json(config, ost, int(result[0][1]), 'conductor')
        except Exception as err:
            logging.error('[-] Произошла ошибка в модуле get_queueitem_conductor: {0}'.format(str(err)))
            exit(0)


def main():
    print('[**] Start data collection')
    logging.info('[**] Сбор данных начат')
    config = read_config('config.json')
    get_win_space(config)
    get_batchparam(config)
    get_queueitem_conductor(config)
    print('[**] Stop data collection')
    logging.info('[**] Сбор данных завершен')


if __name__ == '__main__':
    main()
