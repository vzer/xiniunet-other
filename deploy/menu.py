#!/usr/bin/env python
#coding=utf-8
#版本发布菜单
__author__ = 'vzer'

import sys
import os
import datetime
import re
import string

menuList={}

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

#定义发布版本号函数
def inputVersion():
    version=rawInputColor('green','请输入发布版本号（默认：2.1.0）：')
    if version.strip()=='':
        version='2.1.0'
    while True:
        number=version.strip().split('.')
        if len(number)!=3:
            version=rawInputColor('green','输入的格式错误（参照：2.1.0）：')
        else:
            break
    while not re.search('\d\.\d\.\d',version):
        version=rawInputColor('green','输入的格式错误（参照：2.1.0）：')
    return version

#定义发布版本类型函数
def inputPolicy():
    number=rawInputColor('green','请选择发布版本类型1-SNAPSHOT, 2-RELEASE（默认：SNAPSHOT）：')
    number=filter(str.isdigit,number)
    while True:
        if number.strip()=='':
            policy='SNAPSHOT'
            break
        if int(number)==1:
            policy='SNAPSHOT'
            break
        if int(number)==2:
            policy='RELEASE'
            break
        else:
            number=rawInputColor('green','输入的参数格式错误，（参考：1 2 空）：')
            number=filter(str.isdigit,number)
    return  policy

#定义检查ip地址合法性函数
def checkIp(ipaddr):
    addr = ipaddr.strip().split('.')  #切割IP地址为一个列表
    if len(addr) != 4:  #切割后列表必须有4个参数
        return False
    for i in range(4):
        if addr[i] == "":
            return False
        if not addr[i].isdigit():
            return False
        num = string.atoi(addr[i])
        if num <= 255 and num >= 0:  #每个参数值必须在0-255之间
            continue
        else:
            return False
        i += 1
    return True

#定义ip地址输入函数
def inputIp():
    ipAddress=rawInputColor('green','请输入远端服务器的ip地址（参考：0.0.0.0）：')
    while True:
        flag=checkIp(ipAddress)
        if flag:
            break
        else:
            ipAddress=rawInputColor('green','ip地址输入不合法，请重新输入（参考0.0.0.0）：')
    return  ipAddress

#定义大类菜单选项函数
def bigMenu():
    number=rawInputColor('yellow','Please choice deploy project:1-service, 2-web, 3-queue, 4-job, 5-other [1]:')
    while True:
        if number.strip()=='':
            serviceMethod='service'
            break
        if number=='1':
            serviceMethod='service'
            break
        if number=='2':
            serviceMethod='web'
            break
        if number=='3':
            serviceMethod='queue'
            break
        if number=='4':
            serviceMethod='job'
            break
        if number=='5':
            serviceMethod='other'
            break
        else:
            number=rawInputColor('green','输入的参数格式错误，（参考：1 2 3 4 5 ）：')
    return  serviceMethod

def serviceMenu():
    printColor('yellow','Please choice service task:')
    printColor('yellow','1-foundation')
    printColor('yellow','2-backend')
    printColor('yellow','3-marketplace')
    printColor('yellow','4-platform')
    printColor('yellow','5-financial')
    printColor('yellow','6-distribution')
    printColor('yellow','7-reporting')
    number=rawInputColor('green','service task: [1]')
    serviceList=re.split('\s|\,|\:',number)
    #print serviceList
    for key in  serviceList:
        if key=='1':
            menuList['foundation']=[]
        if key=='2':
            menuList['backend']=[]
        if key=='3':
            menuList['marketplace']=[]
        if key=='4':
            menuList['platform']=[]
        if key=='5':
            menuList['financial']=[]
        if key=='6':
            menuList['distribution']=[]
        if key=='7':
            menuList['reporting']=[]
    list=[]
    for key in menuList:
        printColor('green',key+'参数：')
        list.append(inputVersion())
        list.append(inputPolicy())
        list.append(inputIp())
        menuList[key]=list
        list=[]
    print menuList


if __name__=="__main__":
    choice=bigMenu()
    serviceMenu()
