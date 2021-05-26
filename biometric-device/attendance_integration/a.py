from __future__ import division
import sys
from zklib import zklib, zkconst
import time
import datetime
from datetime import timedelta
import csv
import psycopg2
import math, os
max_time_stamp_check_in=0
max_time_stamp_check_out=0
max_stamp_id_erp=0


zk = zklib.ZKLib("105.112.95.237", 4370)
ret = zk.connect()
print "connection:", ret
if ret == False:
    attendance_list = zk.getAttendance()
    time_record=attendance_list


    # generating csv file
#    os.chmod("/opt/odoo/addons_custom/testing/attendance_integration/csv_files/new_file.csv", 0o777)
    l = open("/opt/odoo/addons_custom/testing/attendance_integration/csv_files/new_file.csv", 'wb')
    print time_record
    for row in time_record:
        i = 0
        time_var = datetime.datetime.now()
        for colunm in row:
            if i != 2:
                l.write('%s;' % colunm)
                i = i + 1

            else:
                time_var = colunm
                l.write('%d;' % time_var.year)
                l.write('%d;' % time_var.month)
                l.write('%d;' % time_var.day)
                l.write('%d;' % time_var.hour)
                l.write('%d;' % time_var.minute)
                l.write('%d;' % time_var.second)

        l.write('\n')
    l.close()
    # end
