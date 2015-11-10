#!/usr/bin/env python
#coding=utf-8
#测试 python-pexpect模块
__author__ = 'vzer'

import sys
import os
import string
import commands
import subprocess
import pexpect

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

def scpWork(localPath,username,host,remotePath):
    #把项目 tar.gz包发送到目标主机上
    scp_NewKeys='.*(yes/no).*'
    scp_passwd='.*assword.*'
    scp_NoFile='No such.*'
    scpTarCmd='scp %s %s@%s:%s' %(localPath,username,host,remotePath)
    print scpTarCmd
    scpChild=pexpect.spawn(scpTarCmd)
    i=scpChild.expect([scp_NewKeys,scp_passwd,scp_NoFile,pexpect.TIMEOUT,pexpect.EOF])
    if i==0:
        scpChild.sendline('yes')
        i=scpChild.expect([scp_NewKeys,scp_passwd,scp_NoFile,pexpect.TIMEOUT,pexpect.EOF])
    if i==1:
        scpChild.sendline('root@xiniu')
        i=scpChild.expect([scp_NewKeys,scp_passwd,scp_NoFile,pexpect.TIMEOUT,pexpect.EOF])
    if i==2:
        printColor('green','scp 上传的文件不存在，请检查版本号，发行系列.')
    if i==3:
        printColor('green','scp 连接超时，请检查网络是否通畅。')
        i=scpChild.expect([scp_NewKeys,scp_passwd,scp_NoFile,pexpect.TIMEOUT,pexpect.EOF])
    if i==4:
        printColor('green','scp 传输完成。')


if __name__=="__main__":
    version='2.1.0'
    policy='SNAPSHOT'
    host='192.168.1.120'
    projectName='foundation'
    localPath='/vzer/service/%s/%s-business/target/%s-business-%s-%s-assembly.tar.gz' %(projectName,projectName,projectName,version,policy)
    username='root'
    remotePath='/xiniu/updateapps'
    scpWork(localPath,username,host,remotePath)