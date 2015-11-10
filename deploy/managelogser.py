#!/usr/bin/env python
#coding=utf-8
#管理flume  kafka  zookeeper
__author__ = 'vzer'

import sys
import os
import re
import string
import subprocess
import paramiko
import pexpect
import pxssh

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


#定义启动flume函数
def startFlume(host):
    username='hadoop'
    passwd='hadoop@xiniu'
    startFlumeCmd='nohup flume-ng agent --conf /home/hadoop/flume/conf -f /home/hadoop/flume/conf/xiniu-module.conf -n collectorMainAgent&'
    sshStarus=sshPexpect(host,username,passwd,startFlumeCmd)

def queryFlume(host):
    username='hadoop'
    passwd='hadoop@xiniu'
    startFlumeCmd='jps -l'
    stdout=sshPxssh(host,username,passwd,startFlumeCmd)
    printColor('green',stdout)
    pid=re.findall(r'(\d+) org.apache.flume.node.Application',stdout)
    print str(pid)
#使用pexpect方式执行ssh
def sshPexpect(ip,username,passwd,cmd):
    stdout = ''
    result = -1
    ssh = pexpect.spawn('ssh %s@%s "%s"' %(username,ip,cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
            print '1'
            ssh.sendline(cmd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
            print '2'
        ssh.sendline(cmd)
        stdout = ssh.read()
        printColor('green',stdout)
        result = 0
    except pexpect.EOF:
        printColor('green','EOF')
        ssh.close()
        result = -1
    except pexpect.TIMEOUT:
        printColor('green','TIMEOUT')
        ssh.close()
        result= -2
    return result,stdout



#使用pxssh方式执行ssh
def sshPxssh(ip,username, passwd,cmd):
    try:
        sshNew=pxssh.pxssh()
        sshNew.login(ip,username,passwd)
        sshNew.sendline(cmd)
        sshNew.prompt()
        return sshNew.before
        sshNew.logout()
    except pxssh.ExceptionPxssh,e:
        printColor('green','pxssh failed on login.')
        printColor('green',str(e))

if __name__=="__main__":
    queryFlume('192.168.1.235')