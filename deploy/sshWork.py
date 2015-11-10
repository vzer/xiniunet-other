#!/usr/bin/env python
#coding=utf-8
#作用 使用paramkio模块做ssh 链接远端主机
__author__ = 'vzer'

import os
import sys
import time
import paramiko
import subprocess
import datetime
import socket

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

#采用 paramiko 上传文件

def putFileWork(localPath,accout,passwd,host,remotePath,filename):
    #检查并建立远端文件夹
    mkFileCmd='mkdir -p '+remotePath
    sshNew=paramiko.SSHClient()
    sshNew.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshNew.connect(host,22,accout,passwd)
    stdin,stdout,stderr=sshNew.exec_command(mkFileCmd)
    for line in stdout:
        printColor('green','...'+line.strip('\n'))
        sshNew.close()
    #上传文件
    remoteHost=(host,22)
    try:
        remoteClient=paramiko.Transport(remoteHost)
        remoteClient.connect(username=accout,password=passwd)
        sshFtp=paramiko.SFTPClient.from_transport(remoteClient)
        print ''
        printColor('green','#########################################')
        printColor('green','Beginning to upload file %s ' % datetime.datetime.now())
        sshFtp.put(localPath+filename,remotePath+filename)
        printColor('green','Upload file success %s ' % datetime.datetime.now())
        print ''
        printColor('green','##########################################' )
        remoteClient.close()
    except paramiko.AuthenticationException,msg:
        printColor('green',msg)
    except socket.error,msg:
        printColor('green',msg)
    except IOError,msg:
        printColor('green',msg)



if __name__=="__main__":
    version='2.1.0'
    policy='SNAPSHOT'
    host='192.168.1.120'
    projectName='foundation'
    filename='webdeploy.sh'
    localPath='/vzer/service/'
    username='root'
    remotePath='/xiniu/scripts/'
    putFileWork(localPath,username,'root@xiniu',host,remotePath,filename)
