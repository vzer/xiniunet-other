#!/usr/bin/env python
#coding=utf-8
#filename:setupFlume.py
__author__ = 'vzer'

import os
import string
import commands
import subprocess
import datetime
import socket
import paramiko
import re
import getpass
import logging
try:
    from pexpect import pxssh
except ImportError,msg:
    print(u'本地环境，无此模块！')
import time

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

#定义log日志
def loger():
    logger=logging.getLogger('setupFlumeLogger')
    logger.setLevel(logging.DEBUG)
    fh=logging.FileHandler('setupFlume.log',mode='w')
    fh.setLevel(logging.DEBUG)

    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s ')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

#采用 paramiko 上传文件
def putFileWork(accout,passwd,host,localPath,remotePath,filename):
    remoteHost=(host,22)
    try:
        remoteClient=paramiko.Transport(remoteHost)
        remoteClient.connect(username=accout,password=passwd)
        sshFtp=paramiko.SFTPClient.from_transport(remoteClient)
        print ''
        printColor('green','###############################################################################')
        print ''
        printColor('green','Beginning to upload file %s ' % datetime.datetime.now())
        sshFtp.put(localPath+filename,remotePath+filename)
        printColor('green','Upload file success %s ' % datetime.datetime.now())
        print ''
        printColor('green','##############################################################################' )
        remoteClient.close()
        return True
    except paramiko.AuthenticationException,msg:
        printColor('green',msg)
        return False
    except socket.error,msg:
        printColor('green',msg)
        return False
    except IOError,msg:
        printColor('green',msg)
        return False

def pxsshWork(hostname,username,password,cmd):
    try:
        sshClient=pxssh.pxssh()
        sshClient.login (hostname, username, password, original_prompt='[$#>]')
        sshClient.sendline (cmd)
        sshClient.prompt()
        result=sshClient.before
        sshClient.logout()
        return (True,result)
    except pxssh.ExceptionPxssh,msg:
        printColor('red',str(msg))
        printColor('red','login failed')
        return (False,msg)
    except Exception,msg:
        printColor('red',str(msg))
        printColor('red','not kown error')
        return  (False,msg)

def queryPid(hostname,username,password,cmd):
    try:
        (status,result)=pxsshWork(hostname,username,password,'jps -l|grep %s'%cmd)
        if  status:
            regex=re.compile('jps -l|grep %s\r\n(.*)\r\n'%cmd).findall(result)
            result=''.join(regex)
            pid=re.findall('(\d+) %s'%cmd,result)
            if pid:
                return ''.join(pid)
            else:
                return ''
        else:
            return ''
    except Exception,msg:
        printColor('red','not kown error')
        printColor('red',str(msg))
        return ''


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


def menu():
     while True:
        printColor('yellow','------------------------------------------------------------------------------')
        printColor('blue','Flume进程相关................')
        printColor('green','1-setup Flume')
        printColor('green','2-Query the Flume status')
        printColor('green','3-Kill the Flume process')
        printColor('green','4-start the Flume process')
        printColor('green','A-restart the Flume process')
        printColor('yellow','------------------------------------------------------------------------------')
        printColor('blue','犀牛后台服务进程相关................')
        printColor('green','5-Query the Service process')
        printColor('green','6-Kill the Service process')
        printColor('green','7-Start the Service process')
        printColor('yellow','------------------------------------------------------------------------------')
        printColor('blue','犀牛前台服务进程相关................')
        printColor('green','8-Query the Web process')
        printColor('green','9-Kill the Web process')
        printColor('green','10-Start the Web process')
        printColor('blue','守护程序运行相关................')
        #printColor('green','11-setup the redis-python')
        printColor('green','12-setup the monitor process')
        #printColor('green','13-Start the Web process')
        choice=rawInputColor('green','you choice(enter q/quit to over):')
        choice=choice.lower()
        if choice=='q' or choice=='quit':
            exit()
        if choice=='1':
            return 1
        elif choice=='2':
            return 2
        elif choice=='3':
            return 3
        elif choice=='4':
            return 4
        elif choice=='5':
            return 5
        elif choice=='6':
            return 6
        elif choice=='7':
            return 7
        elif choice=='8':
            return 8
        elif choice=='9':
            return 9
        elif choice=='10':
            return 10
        elif choice=='a':
            return 'A'


def inputMessage():
    password=''
    username=''
    while True:
        printColor('yellow','###########################################################')
        hostname=inputIp()
        username=rawInputColor('green','username:')
        if len(username)==0:
            username='root'
        password = getpass.getpass('\033[1;32;40mpassword:\033[0m ')
        if len(password)==0:
            password='xiniunet_#2105'
        cmd='hostname'
        (status,result)=pxsshWork(hostname,username,password,cmd)
        if status:
            regex=re.compile('hostname\r\n(.*)\r\n').findall(result)
            printColor('green','登录主机名：%s ------ 登录用户：%s'%(''.join(regex),username))
            return (hostname,username,password)
        else:
            printColor('red','用户名？密码？IP地址错误，请检查')



def setupFlume(hostname,username,password,cmd,name):
    mkdirCmd='mkdir -p /vzer/tools /flume/tmp/flumedir  /flume/tmp/flume_tmp'
    tarCmd='tar zxvf /vzer/tools/flume-client.tar.gz -C /usr/local'
    startCmd='/usr/local/flume/start_flume'
    try:
        printColor('yellow','###########################################################')
        printColor('green','create the runing flume folder  ')
        (status,result)=pxsshWork(hostname,username,password,mkdirCmd)
        if status:
            printColor('green','Create the running folder OK!')
        else:
            printColor('red','Create the running folder ERROR!')
            return False
        printColor('yellow','###########################################################')
        printColor('green','upload The Flume Tar Package To Remote Server. ')
        status=putFileWork(username,password,hostname,localPath,remotePath,filename)
        if status:
            printColor('green',' Upload The Flume Tar OK!')
        else:
            printColor('red',' Upload The Flume Tar ERROR!')
            return False
        printColor('yellow','###########################################################')
        printColor('green','Extract The Flume Tar Package To Runing Folder.')
        (status,result)=pxsshWork(hostname,username,password,tarCmd)
        if status:
            printColor('green','Extract The Flume Tar Package OK!')
        else:
            printColor('red','Extract The Flume Tar Package ERROR!')
            return False
        printColor('yellow','###########################################################')
        printColor('green','Start the flume agent.....  ')
        (status,result)=pxsshWork(hostname,username,password,startCmd)
        if status:
            printColor('green','Start The Flume Agent OK!')
        else:
            printColor('red','Start The Flume Agent ERROR!')
            return False
        printColor('yellow','###########################################################')
        printColor('green','Check The Flume Agent Status.')
        queryProcess(hostname,username,password,cmd,name)
        return True
    except Exception,msg:
        print str(msg)
        return False

def queryProcess(hostname,username,password,cmd,name):
    try:
        pid=queryPid(hostname,username,password,cmd)
        printColor('yellow','###########################################################')
        printColor('yellow','查询%s进程状态'%name)
        if pid:
            printColor('green','The %s Process Running. Pid is %s'%(name,''.join(pid)))
            return True
        else:
            printColor('green','The %s process is Stop.'%name)
            return False
    except Exception,msg:
        printColor('red','not kown error')
        printColor('red',str(msg))
        return False

def killProcess(hostname,username,password,cmd,name):
    try:
        printColor('yellow','###########################################################')
        printColor('yellow','A:查询%s进程状态'%name)
        pid=queryPid(hostname,username,password,cmd)
        if pid:
            printColor('green','The %s Process Running. Pid is %s'%(name,pid))
            killCmd='kill %s'%pid
            printColor('yellow','###########################################################')
            printColor('yellow','B:杀死%s进程'%name)
            (status,result)=pxsshWork(hostname,username,password,killCmd)
            if status:
                printColor('green','Kill The Current Process Command is OK.')
                time.sleep(2)
                printColor('yellow','###########################################################')
                printColor('yellow','C:查询%s进程状态'%name)
                pid=queryPid(hostname,username,password,cmd)
                if pid=='':
                    printColor('green','The %s Process is Stop.'%name)
                    return True
                else:
                    printColor('green','The %s Process Running. Pid is %s'%(name,pid))
                    return False
            else:
                printColor('green','Kill The %s Process Command is ERROR.'%name)
                return False
        else:
            printColor('green','the %s process is Stop.'%name)
    except pxssh.ExceptionPxssh,msg:
        printColor('yellow','###########################################################')
        printColor('red','login failed')
        printColor('red',str(msg))
        return False
    except Exception,msg:
        printColor('yellow','###########################################################')
        printColor('red','not kown error')
        printColor('red',str(msg))
        return False

def startProcess(hostname,username,password,startcmd,querycmd,Name):
    try:
        printColor('yellow','###########################################################')
        printColor('yellow','A:查询%s进程状态'%Name)
        pid=queryPid(hostname,username,password,querycmd)
        if pid=='':
            printColor('green','the %s process is Stop.'%Name)
            printColor('yellow','###########################################################')
            printColor('yellow','B:开启%s进程'%Name)
            (status,result)=pxsshWork(hostname,username,password,startcmd)
            if status:
                printColor('green','Start the %s process command is OK.'%Name)
                time.sleep(2)
                printColor('yellow','###########################################################')
                printColor('yellow','C:查询%s进程状态'%Name)
                pid=queryPid(hostname,username,password,querycmd)
                if pid:
                    printColor('green','The %s Process Running. Pid is %s'%(Name,pid,))
                    return True
                else:
                    printColor('green','the %s process is Stop.'%Name)
                    return False
            else:
                printColor('green','Start the %s process command is ERROR.'%Name)
                return False
        else:
            printColor('green','The %s Process Running. Pid is %s'%(Name,pid))
            return False
    except Exception,msg:
        printColor('yellow','###########################################################')
        printColor('red','not kown error')
        printColor('red',str(msg))
        return False


#开启后台服务，启动日志写到~/start_Service.log
def findServiceCmd(hostname,username,password):
    try:
        (status,result)=pxsshWork(hostname,username,password,'find /xiniu/apps/ -name start.sh')
        if status:
            regex=re.compile('find /xiniu/apps/ -name start.sh\r\n(.*)\r\n').findall(result)
            result=''.join(regex)
            return result
        else:
            return ''
    except Exception,msg:
        printColor('red','not kown error')
        printColor('red',str(msg))
        return ''

if __name__=="__main__":
    #系统登录相关
    username='root'
    password='root@xiniu'
    port=22
    #flume agent 相关
    localPath='/vzer/setupFlume'
    remotePath='/vzer/tools'
    filename='/flume-client.tar.gz'
    FlumeFlag='org.apache.flume.node.Application'
    StartFlumeCmd='/usr/local/flume/start_flume'
    Flumename='Flume'
    #后台服务相关
    ServiceName='Service'
    ServiceFlag='com.alibaba.dubbo.container.Main'
    StartServiceCmd=''
    #前台Web相关
    WebName='Web'
    WebFlag='/usr/jetty/start.jar'
    StartWebCmd='nohup /usr/jetty/bin/jetty.sh start>/dev/null 2>&1 &'

    while True:
        choice=menu()
        hostname,username,password=inputMessage()
        if choice==1:
            setupFlume(hostname,username,password,FlumeFlag,Flumename)
        elif choice==2:
            queryProcess(hostname,username,password,FlumeFlag,Flumename)
        elif choice==3:
            killProcess(hostname,username,password,FlumeFlag,Flumename)
        elif choice==4:
            startProcess(hostname,username,password,StartFlumeCmd,FlumeFlag,Flumename)
        elif choice==5:
            queryProcess(hostname,username,password,ServiceFlag,ServiceName)
        elif choice==6:
            killProcess(hostname,username,password,ServiceFlag,ServiceName)
        elif choice==7:
            StartServiceCmd=findServiceCmd(hostname,username,password)
            if StartServiceCmd=='':
                printColor('red','Not Find Start Service Cmd.')
            else:
                StartServiceCmd='nohup %s>/dev/null 2>&1 &'%StartServiceCmd
                startProcess(hostname,username,password,StartServiceCmd,ServiceFlag,ServiceName)
        elif choice==8:
            queryProcess(hostname,username,password,WebFlag,WebName)
        elif choice==9:
            killProcess(hostname,username,password,WebFlag,WebName)
        elif choice==10:
            startProcess(hostname,username,password,StartWebCmd,WebFlag,WebName)
        else:
            printColor('red','not kown error')
        if rawInputColor('yellow','按ENTER键继续........'):
            pass





