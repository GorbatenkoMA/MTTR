#!/root/venv/my_env/bin/python3.6
#-*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

template_mttr = '''
Кол-во инфраструктурных инцидентов: {}
Целевое значение MTTR, мин:         {}
Суммарное время простоя, мин:       {} 
MTTR расчитанное, мин:              {}
Итоговое значение КПЭ %:            {}
Необходимое кол-во инцидентов для достижения целевого показателя: {}
'''

def index_row(line):
    l = line.strip().split(';')
    return l.index('Номер'), l.index('Время направления в работу'), l.index('Время закрытия события в системе мониторинга')

def calc_mttr(espp_file = 'export.csv', target_mttr = 130):
    with open(espp_file, 'r') as f:
        sum_time_all_incident = 0
        count_incident = 0
        first_line = True
        for line in f:
            if first_line:
                index_num_incident, index_time_work, index_close = index_row(line)
                first_line = False
            else:            
                incident = line.strip().split(';')
                if incident != [''] and incident[index_time_work].replace('"','') != '' and incident[index_close].replace('"','') != '':
                    count_incident += 1            
                    time_ref_to_work        = datetime.strptime(incident[index_time_work].replace('"',''), '%d/%m/%y %H:%M:%S')
                    time_close_monit_system = datetime.strptime(incident[index_close].replace('"',''), '%d/%m/%y %H:%M:%S')
                    sum_time_all_incident   = sum_time_all_incident + (time_close_monit_system - time_ref_to_work).total_seconds()

        print(template_mttr.format(count_incident,
                                   target_mttr,
                                   int((sum_time_all_incident / 60)),
                                   int((sum_time_all_incident / 60) / count_incident),
                                   int((target_mttr / ((sum_time_all_incident / 60) / count_incident)) * 100),
                                   int((count_incident * target_mttr)/((sum_time_all_incident / 60) / count_incident)) + count_incident))

calc_mttr()

