#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import re
import paramiko
import socket
import datetime
import subprocess
from config import ProducePlatformServiceIp as ServiceIp
from config import ProducePlatformWebIp as WebIp
from config import ProducePlatformJobIp as JobIp
from config import user,password
from config import proplatserviceLocalPath as serviceLocalPath
from config import proplatserviceScriptFile as serviceScriptFile
from config import proplatwebScriptFile as webScriptFile
from config import proplatwebLocalPath as webLocalPath
from config import proplatjobLocalPath as jobLocalPath
from config import proplatjobScriptFile as jobScriptFile

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

#定义发布版本号函数
def inputVersion():
    version=rawInputColor('yellow','please enter the version number(default:1.0.0):')
    if version.strip()=='':
        version='1.0.0'
    while True:
        number=version.strip().split('.')
        if len(number)!=3:
            version=rawInputColor('red','the version format is ERROR!!(as:1.0.0)')
        else:
            break
    while not re.search('\d\.\d\.\d',version):
        version=rawInputColor('the version format is ERROR!!(as:1.0.0)')
    return version

#定义autoconfig是否采用交互模式
def swapMode():
    mode=rawInputColor("yellow",'do you want use Interactive mode for autoconfig(yes/no,default:no): ')
    if mode.strip()=="":
        mode="no"
    if mode in("YES","yes","Y","y"):
        return "yes"
    else:
        return "no"

#采用 paramiko 上传文件
def putFileWork(accout,passwd,host,localPath,remotePath,filename,scriptFile):
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
        sshFtp.put(localPath+scriptFile,remotePath+scriptFile)
        printColor('green','Upload file success %s ' % datetime.datetime.now())
        print ''
        printColor('green','##########################################' )
        remoteClient.close()
        return True
    except paramiko.AuthenticationException,msg:
        printColor('red',msg)
        printColor("red","login the remote server FAILURE！！！，plaese check the username and password")
        return False
    except socket.error,msg:
        printColor('red',msg)
        printColor("red","Transfer files fails(socket), please re-transmission!!")
        return False
    except IOError,msg:
        printColor('red',msg)
        printColor("red","Transfer files fails(IO), please re-transmission!!")
        return False
    except OSError,msg:
        printColor('red',msg)
        printColor("red","Transfer file does not exist, please check the file!!!")
        return False


#后台服务发布方法
def serviceDeploy():
    while True:
        for select in range(len(ServiceIp)):
            printColor("green","%s-%s"%(select,''.join(ServiceIp[select].keys())))
        choice=rawInputColor("yellow","please choice the service of task(/quit):")

        if choice in ("quit","QUIT","q","Q"):
            break

        if choice.isdigit()and (int(choice)>=0 and int(choice)<len(ServiceIp)):
            version=inputVersion()
            mode=swapMode()
            for key,value in ServiceIp[int(choice)].items():
                while True:
                    for value2 in range(len(value)):
                        printColor("green","%s-%s:%s"%(value2,key,value[value2]))
                    choice1=rawInputColor("yellow","please choice the deploy host(/quit):")
                    if choice1 in ("quit","QUIT","q","Q"):
                        break
                    if choice1.isdigit()and (int(choice1)>=0 and int(choice1)<len(value)):
                        printColor("purple","the Deployment of service:%s"%key)
                        printColor("purple","the Deployment of host:%s"%value[int(choice1)])
                        printColor("purple","the Deployment of version:%s"%version)
                        printColor("purple","use the Deployment of AutoConfig Interactive mode:%s"%mode)
                        filename="%s-business-%s-assembly.tar.gz"%(key,version)
                        putFileStatus=putFileWork(user,password,value[int(choice1)],serviceLocalPath,serviceLocalPath,filename,serviceScriptFile)
                        if putFileStatus==True:
                            try:
                                subprocess.check_call('ssh %s@%s sh %s/%s %s %s %s'%(user,value[int(choice1)],serviceLocalPath,serviceScriptFile,key,version,mode),shell=True)
                            except subprocess.CalledProcessError,msg:
                                printColor('red',msg)
                                printColor("red","User name or password is incorrect, please check!!")
                        choice3=rawInputColor("yellow","do you want need deploy the next %s host?(yes/no/quit):"%key)
                        if choice3 in ("yes","y","YES","Y"):
                            continue
                        elif choice3 in ("quit","QUIT","Q","q"):
                            exit()
                        elif choice3 in("no","NO","N","n"):
                            break
                        else:
                            rawInputColor("red","Entry ERROR, press the Enter to continue！！")
                    else:
                        rawInputColor("red","Entry ERROR, press the Enter to continue！！")
        else:
            rawInputColor("red","Entry ERROR, press the Enter to continue！！")


#前台web发布方法
def webDeploy():
    while True:
        for select in range(len(WebIp)):
            printColor("green","%s-%s"%(select,''.join(WebIp[select].keys())))
        choice=rawInputColor("yellow","please choice the service of task(/quit)：")
        if choice in ("quit","QUIT","q","Q"):
            break
        if choice.isdigit()and (int(choice)>=0 and int(choice)<len(WebIp)):
            version=inputVersion()
            mode=swapMode()
            for key,value in WebIp[int(choice)].items():
                while True:
                    for value2 in range(len(value)):
                        printColor("green","%s-%s:%s"%(value2,key,value[value2]))
                    choice1=rawInputColor("yellow","please choice the deploy host(/quit):")
                    if choice1 in ("quit","QUIT","q","Q"):
                        break
                    if choice1.isdigit()and (int(choice1)>=0 and int(choice1)<len(value)):
                        printColor("purple","the Deployment of service:%s"%key)
                        printColor("purple","the Deployment of host:%s"%value[int(choice1)])
                        printColor("purple","the Deployment of version:%s"%version)
                        printColor("purple","use the Deployment of AutoConfig Interactive mode:%s"%mode)
                        filename="%s-%s.war"%(key,version)
                        putFileStatus=putFileWork(user,password,value[int(choice1)],webLocalPath,webLocalPath,filename,webScriptFile)
                        if putFileStatus==True:
                            try:
                                subprocess.check_call('ssh %s@%s sh %s/%s %s %s %s'%(user,value[int(choice1)],webLocalPath,webScriptFile,key,version,mode),shell=True)
                            except subprocess.CalledProcessError,msg:
                                printColor('red',msg)
                                printColor("red","User name or password is incorrect, please check!!")
                        choice3=rawInputColor("yellow","do you want need deploy the next %s host?(yes/no/quit):"%key)
                        if choice3 in ("yes","y","YES","Y"):
                            continue
                        elif choice3 in ("quit","QUIT","Q","q"):
                            exit()
                        elif choice3 in("no","NO","N","n"):
                            break
                        else:
                            rawInputColor("red","Entry ERROR, press the Enter to continue！！")
                    else:
                        rawInputColor("red","Entry ERROR, press the Enter to continue！！")
        else:
            rawInputColor("red","Entry ERROR, press the Enter to continue！！")


#定时脚本发布方法
def jobDeploy():
    while True:
        for select in range(len(JobIp)):
            printColor("green","%s-%s"%(select,''.join(JobIp[select].keys())))
        choice=rawInputColor("yellow","please choice the service of task(/quit)：")
        if choice in ("quit","QUIT","q","Q"):
            break
        if choice.isdigit()and (int(choice)>=0 and int(choice)<len(JobIp)):
            version=inputVersion()
            mode=swapMode()
            for key,value in JobIp[int(choice)].items():
                while True:
                    for value2 in range(len(value)):
                        printColor("green","%s-%s:%s"%(value2,key,value[value2]))
                    choice1=rawInputColor("yellow","please choice the deploy host(/quit):")
                    if choice1 in ("quit","QUIT","q","Q"):
                        break
                    if choice1.isdigit()and (int(choice1)>=0 and int(choice1)<len(value)):
                        printColor("purple","the Deployment of service:%s"%key)
                        printColor("purple","the Deployment of host:%s"%value[int(choice1)])
                        printColor("purple","the Deployment of version:%s"%version)
                        printColor("purple","use the Deployment of AutoConfig Interactive mode:%s"%mode)
                        filename="%s-%s-assembly.tar.gz"%(key,version)
                        putFileStatus=putFileWork(user,password,value[int(choice1)],jobLocalPath,jobLocalPath,filename,jobScriptFile)
                        if putFileStatus==True:
                            try:
                                subprocess.check_call('ssh %s@%s sh %s/%s %s %s %s'%(user,value[int(choice1)],jobLocalPath,jobScriptFile,key,version,mode),shell=True)
                            except subprocess.CalledProcessError,msg:
                                printColor('red',msg)
                                printColor("red","User name or password is incorrect, please check!!")
                        choice3=rawInputColor("yellow","do you want need deploy the next %s host?(yes/no/quit):"%key)
                        if choice3 in ("yes","y","YES","Y"):
                            continue
                        elif choice3 in ("quit","QUIT","Q","q"):
                            exit()
                        elif choice3 in("no","NO","N","n"):
                            break
                        else:
                            rawInputColor("red","Entry ERROR, press the Enter to continue！！")
                    else:
                        rawInputColor("red","Entry ERROR, press the Enter to continue！！")
        else:
            rawInputColor("red","Entry ERROR, press the Enter to continue！！")



if __name__ == '__main__':
    while True:
        select=rawInputColor("yellow","Please choice deploy project:1-service,2-Web,3-Job(1/2/3/quit)")
        if select=="1":
            serviceDeploy()
        elif select=="2":
            webDeploy()
        elif select=="3":
            jobDeploy()
        elif select in ("quit","QUIT","q","Q"):
            printColor("green","Bai,Bai!")
            exit()
        else:
            select=rawInputColor("red","Entry ERROR, press the Enter to continue！！")
            continue
