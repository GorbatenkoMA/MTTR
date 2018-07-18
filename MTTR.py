#!/root/venv/my_env/bin/python3.6
#-*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

template_mttr = '''
Суммарное время простоя в мин:      {} 
Кол-во инфраструктурных инцидентов: {}
Целевое значение MTTR мин:          {}  
MTTR мин:                           {}
Итоговое значение КПЭ %:            {}
'''

def index_row(line):
    l = line.strip().split(';')
    return l.index('Номер'), l.index('Время направления в работу'), l.index('Время закрытия события в системе мониторинга')

with open('export.csv', 'r') as f:
    target_mttr = 130
    sum_time_all_incident = 0
    count_incident = 0
    first_line = True
    for line in f:
        if first_line:
            index_num_incident, index_time_work, index_close = index_row(line)
            first_line = False
        else:            
            incident = line.strip().split(';')
            if incident != [''] and incident[index_time_work] != '' and incident[index_close] != '':
                count_incident += 1
                time_ref_to_work        = datetime.strptime(incident[index_time_work], '%d.%m.%Y %H:%M')
                time_close_monit_system = datetime.strptime(incident[index_close], '%d.%m.%Y %H:%M')
                sum_time_all_incident   = sum_time_all_incident + (time_close_monit_system - time_ref_to_work).total_seconds()

    print(template_mttr.format(int((sum_time_all_incident / 60)),
                               count_incident, 
                               target_mttr,
                               int((sum_time_all_incident / 60) / count_incident),
                               int((target_mttr / ((sum_time_all_incident / 60) / count_incident)) * 100)))




            




