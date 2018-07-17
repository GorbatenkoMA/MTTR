#!/root/venv/my_env/bin/python3.6
#-*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

template_mttr = '''
            Кол-во инфраструктурных инцидентов: {}
            MTTR                                {}
            '''

with open('export.csv', 'r') as f:
    sum_time_all_incident = 0
    count_incident = 0
    for line in f:
        incident = line.strip().split(';')
        if 'ИНЦ' in incident[0]:
            count_incident += 1
            time_ref_to_work = datetime.strptime(incident[1], '%d.%m.%Y %H:%M')
            time_close_monit_system = datetime.strptime(incident[2], '%d.%m.%Y %H:%M')
            sum_time_all_incident = sum_time_all_incident + (time_close_monit_system - time_ref_to_work).total_seconds()
    print(template_mttr.format(count_incident, int((sum_time_all_incident / 60) / count_incident)))




            




