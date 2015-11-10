#!/usr/bin/env python
#coding=utf-8
#flume的开启，查询 关闭
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
def queryFlume():
    try:
        output=subprocess.check_output('jps',shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)



#开启flume
def startFlume():
    startCmd=' nohup /usr/local/flume/bin/flume-ng agent --conf /usr/local/flume/conf/ -f /usr/local/flume/conf/xiniu-module.conf -n collectorMainAgent &'
    try:
        output=subprocess.check_output(startCmd,shell=True)
        printColor('green',output)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#关闭Flume
def stopFlume():
    try:
        output=subprocess.check_output('jps',shell=True)
        pid=re.findall('(\d+) Application',output)
        killCmd='kill -9 %s' %''.join(pid)
        killOutput=subprocess.check_call(killCmd,shell=True)
        printColor('green',killOutput)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)


if __name__=="__main__":
    printColor('yellow','Please Choice Flume Task[q/quit]:')
    printColor('yellow','1-query Flume Status')
    printColor('yellow','2-Start Flume')
    printColor('yellow','3-Stop Flume')
    number=rawInputColor('green','Flume Task[q/quit]:')
    while True:
        number=number.lower()
        if number=='q'or number=='quit':
            printColor("green",'quit.....')
            exit(0)
        elif number=='1':
            queryFlume()
            number=rawInputColor('green','Again Flume Task[q/quit]:')
            printColor('yellow','1-query Flume Status')
            printColor('yellow','2-Start Flume')
            printColor('yellow','3-Stop Flume')
        elif number=='2':
            startFlume()
            number=rawInputColor('green','Again Flume Task[q/quit]:')
            printColor('yellow','1-query Flume Status')
            printColor('yellow','2-Start Flume')
            printColor('yellow','3-Stop Flume')
        elif number=='3':
            stopFlume()
            number=rawInputColor('green','Again Flume Task[q/quit]:')
            printColor('yellow','1-query Flume Status')
            printColor('yellow','2-Start Flume')
            printColor('yellow','3-Stop Flume')
        else:
            number=rawInputColor('green','input is error please again[q/quit]:')
            break

