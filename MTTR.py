#!/root/venv/my_env/bin/python3.6
#-*- coding: utf-8 -*-

# mount -t cifs //10.10.1.141/mttr /mnt/mttr -o user=cisco,password=cisco 

from datetime import datetime
from datetime import timedelta
from operator import itemgetter
import os
import glob
import codecs

template_mttr = '''
Кол-во инфраструктурных инцидентов: {}
Целевое значение MTTR, мин:         {}
Суммарное время простоя, мин:       {} 
MTTR расчитанное, мин:              {}
Итоговое значение КПЭ %:            {}
'''
dict_mttr = {'count_incident': None,
           'target_mttr': None,
           'sum_time_all_incident': None,
           'mttr': None,
           'kpe': None,
           'count_incident_to_target_mttr': None,
           'dict_incident': {}}

def index_row(line):
    l = line.strip().split(';')
    return l.index('Номер'), l.index('Время направления в работу'), l.index('Время закрытия события в системе мониторинга')

def last_modified_file(folder):
    files = list(filter(os.path.isfile, glob.glob(folder + "/*")))
    if len(files) > 0:
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return files[0]
    else:
        return None

def calc_mttr(espp_file = 'export.csv', target_mttr = 130):
#    with open(espp_file, 'r') as f:
    with codecs.open(espp_file, 'r', encoding='windows-1251') as f:
        sum_time_all_incident = 0
        count_incident = 0
        first_line = True
        for line in f:
            #print(line)
            if first_line:
                index_num_incident, index_time_work, index_close = index_row(line)
                first_line = False
            else:            
                incident = line.strip().split(';')
                if incident != [''] and incident[index_time_work].replace('"','') != '' and incident[index_close].replace('"','') != '':
                    count_incident += 1            
                    time_ref_to_work        = datetime.strptime(incident[index_time_work].replace('"',''), '%d/%m/%y %H:%M:%S')
                    time_close_monit_system = datetime.strptime(incident[index_close].replace('"',''), '%d/%m/%y %H:%M:%S')
                    sum_time_all_incident = sum_time_all_incident + ((time_close_monit_system - time_ref_to_work).total_seconds())/60 # в минутах
                    dict_mttr['dict_incident'][incident[index_num_incident]] = int(((time_close_monit_system - time_ref_to_work).total_seconds())/60)

    dict_mttr['count_incident'] = int(count_incident)
    dict_mttr['target_mttr'] = target_mttr
    dict_mttr['sum_time_all_incident'] = int(sum_time_all_incident)
    dict_mttr['mttr'] = int(sum_time_all_incident / count_incident)
    dict_mttr['kpe'] = int((target_mttr / (sum_time_all_incident / count_incident)) * 100)
    #dict_mttr['count_incident_to_target_mttr'] = int((count_incident * target_mttr) / (sum_time_all_incident / count_incident) + count_incident)

    return dict_mttr

d = calc_mttr(last_modified_file('/mnt/mttr/'))

print(template_mttr.format(d['count_incident'], d['target_mttr'], d['sum_time_all_incident'], d['mttr'], d['kpe'], d['count_incident_to_target_mttr']))

print('{:20}{:15} {}\n'.format('Инцидент', 'Время_простоя', 'Процент_влияния_на_mttr'))

for k,v in sorted(d['dict_incident'].items(), key=itemgetter(1), reverse=True):
    print('{}  {:8}  {:15.2f}'.format(k.replace('"',''), v, ((v * 100) / d['sum_time_all_incident'])))
     

