from os import makedirs
from datetime import datetime

import csv

def log_socket_communication(time, net, cmd, ret_msg) :
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    y = time.year
    m = time.month
    d = time.day
    h = time.hour
    path = f'./Command_Log/{net}/{y}/{m}/{d}/'

    try : 
        with open(f'{path}{h}.csv','a+') as f :
            writer = csv.writer(f)
            writer.writerow([t, cmd, ret_msg])

    except OSError :
        makedirs(path)
        with open(f'{path}{h}.csv','a+') as f :
            writer = csv.writer(f)
            writer.writerow([t, cmd, ret_msg])
