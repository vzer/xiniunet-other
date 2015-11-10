#!/usr/bin/env python
#coding=utf-8
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

#查询进程JPS
def queryJps():
    try:
        output=subprocess.check_output('js',shell=True)
        print type(output)
        pid=re.findall('(\d+) Application',output)
        print pid
        print type(pid)
        killCmd='kill -9 %s' %''.join(pid)
        print  killCmd
        #killoutput=subprocess.check_output(killCmd,shell=True)
    except subprocess.CalledProcessError,msg:
        print msg




if __name__=="__main__":

    #startNimbusCmd='/usr/local/storm/bin/storm nimbus >/dev/null 2>&1 &'
    #startSupervisorCmd='/usr/local/storm/bin/storm supervisor>/dev/null 2>&1 &'
    #startStormUi='/usr/local/storm/bin/storm ui >/dev/null 2>&1 &'
    '''nimbusStatus=subprocess.check_call(startNimbusCmd,shell=True)
    if int(nimbusStatus)==0:
        printColor('green','start flume ok.')
    else:
        printColor('green','start flume error')
    '''
    #supervisorStatus=subprocess.check_call(startSupervisorCmd,shell=True)
    #if int(supervisorStatus)==0:
        #printColor('green','start nimbus ok.')
    #else:
        #printColor('green','start nimbus error.')
    '''uiStatus=subprocess.check_call(startStormUi,shell=True)
    if int(uiStatus)==0:
        printColor('green','start storm ui ok')
    else:
        printColor('green','start storm ui error')
    '''
    queryJps()
