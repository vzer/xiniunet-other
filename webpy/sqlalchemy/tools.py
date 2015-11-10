#!/usr/bin/env python
# _*_ coding:utf8 _*_
__author__ = 'vzer'

from pexpect import pxssh
import re
import os
import sys
import subprocess
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
import setting
from multiprocessing import Process

Base=declarative_base()

class ServerInfo(Base):
    __tablename__='serverinfo'
    id=Column(Integer,primary_key=True,autoincrement=True)
    hostname=Column(String(50))
    ip=Column(String(50))
    account=Column(String(50))
    password=Column(String(50))
    servicename=Column(String(50))


ksession=setting.DBsession()

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

def shellCmd(cmd):
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (processStdout,processStderr) = process.communicate()
    retcode = process.poll()
    if retcode:
        return (retcode,processStderr)
    return (retcode,processStdout)

def pxsshWork(hostname,username,password,cmd):
    try:
        sshClient=pxssh.pxssh()
        sshClient.login (hostname, username, password, original_prompt='[$#>]')
        sshClient.sendline (cmd)
        print cmd
        sshClient.prompt()
        result=sshClient.before
        sshClient.logout()
        return (True,result)
    except pxssh.ExceptionPxssh,msg:
        printColor('red',str(msg))
        printColor('red','login failed')
        return (False,msg)

#开启后台服务，启动日志写到~/start_Service.log
def findServiceCmd(hostname,username,password):
    try:
        (status,result)=pxsshWork(hostname,username,password,'find /xiniu/apps/ -name start.sh |sort -M')
        if status:
            regex=re.compile('find /xiniu/apps/ -name start.sh |sort -M\r\n(.*)\r\n').findall(result)
            result=''.join(regex)
            return result
        else:
            return ''
    except Exception,msg:
        printColor('red','not kown error')
        printColor('red',str(msg))
        return ''

def startTask(*args):
    print os.getpid()
    for ip in xrange(args[1],args[2]):
        #(status,result)=shellCmd('fping 192.168.1.%s'%ip)
        result='192.168.1.130 is alive'
        print result
        if 'alive' in result:
            (status,result)=pxsshWork('192.168.1.%s'%ip,'root','root@xiniu','hostname')
            if status:
                regex=re.compile('hostname\r\n(.*)\r\n').findall(result)
                hostname=''.join(regex)
                print  hostname
                result=findServiceCmd('192.168.1.%s'%ip,'root','root@xiniu')
                if 'start.sh' in result:
                    result=result.split('/')
                    print  result[3]
                    info=ServerInfo(hostname=hostname,ip='192.168.1.%s'%ip,account='root',password='root@xiniu',servicename=str(result[3]))
                    ksession.add(info)
    ksession.commit()
    ksession.close()

if __name__ == '__main__':
    startTask(sys.argv[1:])