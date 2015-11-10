#!/usr/bin/env python
#coding=utf-8
#storm的开启，查询 关闭
__author__ = 'vzer'

import subprocess
import re


'''
功能：有色输出
参数：
    color:颜色代码
        "Red,Yellow,Blue,Green"
    text:要输出的文本
	flag:输出不换行标识
返回值：
    None

'''
def printColor(color,text,flag = False):
	colour = color.lower()
	if colour == 'red':
		if flag:
			iText = '\033[1;31;40m%s\033[0m' %text
			print (iText),
		else:
			print '\033[1;31;40m%s\033[0m' %text
	elif colour == 'yellow':
		if flag:
			iText = '\033[1;33;40m%s\033[0m'
			print (iText),
		else:
			print '\033[1;33;40m%s\033[0m' %text
	elif colour == 'blue':
		if flag:
			iText = '\033[1;34;40m%s\033[0m' %text
			print (iText),
		else:
			print '\033[1;34;40m%s\033[0m' %text
	elif colour == 'green':
		if flag:
			iText = '\033[1;32;40m%s\033[0m' %text
			print (iText),
		else:
			print '\033[1;32;40m%s\033[0m' %text
	elif colour == 'purple':
		if flag:
			iText = '\033[1;35;40m%s\033[0m' %text
			print (iText),
		else:
			print '\033[1;35;40m%s\033[0m' %text
	else:
		print text

'''
功能：有色输入
参数：
    color:颜色代码
        "Red,Yellow,Blue,Green"
    text:要输出的文本
	flag:输出不换行标识
返回值：
    None

'''
def rawInputColor(color,text):
    colour = color.lower()
    if colour == 'red':
        iText = '\033[1;31;40m%s\033[0m' %text
    elif colour == 'yellow':
        iText = '\033[1;33;40m%s\033[0m' %text
    elif colour == 'blue':
		iText = '\033[1;34;40m%s\033[0m' %text
    elif colour == 'green':
        iText = '\033[1;32;40m%s\033[0m' %text
    elif colour == 'purple':
		iText = '\033[1;35;40m%s\033[0m' %text
    else:
        return raw_input(text)
    return raw_input(iText)

#查询进程
def queryStorm():
    try:
        output=subprocess.check_output('jps',shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)



#开启nimbus
def startNimbus():
    startCmd=' /usr/local/storm/bin/storm nimbus >/dev/null 2>&1 &'
    try:
        output=subprocess.check_output(startCmd,shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
#开启supervisor
def startSupervisor():
    startCmd=' /usr/local/storm/bin/storm supervisor >/dev/null 2>&1 &'
    try:
        output=subprocess.check_output(startCmd,shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#开启stormUi
def startStormUi():
    startCmd=' /usr/local/storm/bin/storm ui >/dev/null 2>&1 &'
    try:
        output=subprocess.check_output(startCmd,shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#开启 strom jar
def startStromTop():
    startCmd='/usr/local/storm/bin/storm jar storm-kafka-integration-1.0.0-SNAPSHOT-jar-with-dependencies.jar  com.xiniunet.stormkafka.MyKafkaTopology 10.117.208.216'
    try:
        output=subprocess.check_output(startCmd,shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#开启strom 全部模块
def startStormAll():
    try:
        startNimbus()
        startSupervisor()
        startStormUi()
        startStromTop()
    except subprocess.CalledProcessError,msg:
        printColor('green',msg)

#关闭nimbus
def stopNimbus():
    try:
        output=subprocess.check_output('jps',shell=True)
        pid=re.findall('(\d+) nimbus',output)
        killCmd='kill -9 %s' %''.join(pid)
        killOutput=subprocess.check_call(killCmd,shell=True)
        printColor('green',killOutput)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#关闭supervisor
def stopSupervisor():
    try:
        output=subprocess.check_output('jps',shell=True)
        pid=re.findall('(\d+) supervisor',output)
        killCmd='kill -9 %s' %''.join(pid)
        killOutput=subprocess.check_call(killCmd,shell=True)
        printColor('green',killOutput)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#关闭Storm Ui
def stopStormUi():
    try:
        output=subprocess.check_output('jps',shell=True)
        pid=re.findall('(\d+) core',output)
        killCmd='kill -9 %s' %''.join(pid)
        killOutput=subprocess.check_call(killCmd,shell=True)
        printColor('green',killOutput)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#关闭Storm All
def stopStormAll():
    try:
        stopNimbus()
        stopSupervisor()
        stopStormUi()
    except subprocess.CalledProcessError,msg:
        printColor('green',msg)

#定义菜单
def menu():
    printColor('yellow','1-query Storm Status')
    printColor('yellow','2-Start All Module Of Storm ')
    printColor('yellow','3-Start Nimbus')
    printColor('yellow','4-Start Supervisor')
    printColor('yellow','5-Start Storm Ui')
    printColor('yellow','6-Start Storm Jar')
    printColor('yellow','7-Stop All Module Of Storm ')
    printColor('yellow','8-Stop Nimbus')
    printColor('yellow','9-Stop Supervisor')
    printColor('yellow','10-Stop Storm Ui')

if __name__=="__main__":
    printColor('yellow','Please Choice Storm Task[q/quit]:')
    menu()
    number=rawInputColor('green','Storm Task[q/quit]:')
    while True:
        number=number.lower()
        if number=='q'or number=='quit':
            printColor("green",'quit.....')
            exit(0)
        elif number=='1':
            queryStorm()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='2':
            startStormAll()
            number=rawInputColor('green','Again Strom Task[q/quit]:')
            menu()
        elif number=='3':
            startNimbus()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='4':
            startSupervisor()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='5':
            startStormUi()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='6':
            startStromTop()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='7':
            stopStormAll()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='8':
            stopNimbus()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='9':
            stopSupervisor()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        elif number=='10':
            stopStormUi()
            number=rawInputColor('green','Again Storm Task[q/quit]:')
            menu()
        else:
            menu()
            number=rawInputColor('green','input is error please again[q/quit]:')



