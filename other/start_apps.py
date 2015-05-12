#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath)

from common.common import Common,connect_device,createlogger

def start_apps(appflie ='applist.txt'):
    #serino = "MDEVICE"
    serino = "e5a8e6d3"
    if len(sys.argv)>1:       
        serino = sys.argv[1] 
    mod = Common(serino, "Tasking") 
    f = open(appflie)
    Info()
    for name in f.readlines():     
        #print name.strip()
        mod.start_app(name.strip())
        Info()
    f.close()

def Info():
    meminfo=os.popen("adb shell dumpsys meminfo").readlines()
    for memory in meminfo:
        Total_RAM=re.match(r'Total RAM: (\d+)',memory.strip())
        if Total_RAM is not None:
            print 'Total_memory:%dKB'%int(Total_RAM.group(1))
        Free_RAM=re.match(r'Free RAM: (\d+)',memory.strip())
        if Free_RAM is not None:
            print 'Free_memory:%dKB'%int(Free_RAM.group(1))
        Used_RAM=re.match(r'Used RAM: (\d+)',memory.strip())
        if Used_RAM is not None:
            print 'Used_memory:%dKB'%int(Used_RAM.group(1))  
    battery_temp=os.popen("adb shell cat /sys/class/power_supply/battery/uevent")
    for info in battery_temp:
        temp=re.match(r'POWER_SUPPLY_TEMP=(\d+)',info.strip())
        if temp is not None:
            print "Battery_temp=%0.1f"%(float(temp.group(1))/10)
    top=os.popen("adb shell top -n 1").readlines()
    for data in top:
        m=re.match("(User)",data.strip())
        if m is not None:
            print "CPU:%s"%(data)
            break
def main():
    start_apps()

if __name__ == '__main__':
    main()





 





'''功能增加如下：
    统计当前系统占用内存有多少，用户内存多少，可用内存多少， CPU 频率， CPU 温度值，当前电池温度值。
每次启动应用前和后都统计一次。'''
  
