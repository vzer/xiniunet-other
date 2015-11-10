#!/usr/bin/env python
#coding=utf-8
#filename:deploy.py
__author__ = 'vzer'

import sys
import os
import string
import commands
import subprocess
import pexpect
import datetime
import socket
import paramiko
import re
import getpass
import logging

#定义运行环境参数
deployDict={}
deployDict['userName']='root'
deployDict['passwd']='root@xiniu'
deployDict['remoteTarPath']='/vzer/updateapps/'
deployDict['remoteScriptPath']='/vzer/scripts/'
deployDict['localServicePath']='/vzer/service/'
deployDict['localWebPath']='/vzer/web/'
deployDict['shellScriptFile']='webdeploy.sh'

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

#定义修改用户名函数
def changeUser():
    userName=rawInputColor('green','请输入账户名（默认root）：')
    if userName.strip()=='':
        userName='root'
    while not re.search('[a-zA-z0-9]+',userName):
        userName=rawInputColor('green','输入账户名格式错误（参考：root）:')
    return userName
#定义修改密码函数
def changePasswd():
    passwd=getpass.getpass('\033[1;32;40m请输入密码（默认admin）:\033[0m')
    if passwd.strip()=='':
        passwd='root@xiniu'
    return passwd
#定义修改远端打包文件目录函数
def changeRemoteTarPath():
    remoteTarPath=rawInputColor('green','请输入远端的tar打包文件路径（默认/xiniu/updataapps/）:')
    if remoteTarPath.strip()=='':
        remoteTarPath='/xiniu/updateapps/'
    while not re.search('\/.*\/.*\/',remoteTarPath):
        remoteTarPath=rawInputColor('green','输入远端的tar打包文件路径格式错误（参考：/xiniu/updataapps/）:')
    return remoteTarPath
#定义修改远端执行脚本目录函数
def changeRemoteScriptPath():
    remoteScriptPath=rawInputColor('green','请输入远端的script打包文件路径（默认/xiniu/scripts/）:')
    if remoteScriptPath.strip()=='':
        remoteScriptPath='/xiniu/scripts/'
    while not re.search('\/.*\/.*\/',remoteScriptPath):
        remoteScriptPath=rawInputColor('green','输入远端的script打包文件路径格式错误（参考：/xiniu/scripts/）:')
    return remoteScriptPath
#定义修改本地service打包项目存放目录函数
def changeLocalServicePath():
    localServicePath=rawInputColor('green','请输入本地service项目路径（默认：/vzer/service/）:')
    if localServicePath.strip()=='':
        localServicePath='/vzer/service/'
    while not re.search('\/.*\/.*\/',localServicePath):
        localServicePath=rawInputColor('green','输入本地service项目存放路径格式错误（参考：/vzer/service/）:')
    return  localServicePath
#定义修改本地web打包项目存放目录函数
def changeLocalWebPath():
    localWebPath=rawInputColor('green','请输入本地Web项目存放路径（默认：/vzer/web/）:')
    if localWebPath.strip()=='':
        localWebPath='/vzer/web/'
    while not re.search('\/.*\/.*\/',localWebPath):
        localWebPath=rawInputColor('green','输入本地Web项目存放路径格式错误（参考：/vzer/web/）:')
    return  localWebPath
#定义修改远端执行脚本文件名函数
def changeShellScript():
    shellScript=rawInputColor('green','请出入远端执行sh脚本(默认：webdeploy.sh):')
    if shellScript.strip()=='':
        shellScript='webdeploy.sh'
    while not re.search('.*\.sh',shellScript):
        shellScript=rawInputColor('green','输入格式错误(参照：webdeploy.sh):')
    return shellScript

#定义创建本地文件夹函数
def makeDir(path):
    try:
        mkdirCmd='mkdir -p '+path
        mkdirStatus=subprocess.check_call(mkdirCmd,shell=True)
        if mkdirStatus=='0':
            return True
        else:
            return False
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
#定义删除本地文件夹函数
def rmDir(path):
    rmDirCmd='sudo rm -rf %s' %path
    try:
        rmDirStatus=subprocess.check_call(rmDirCmd,shell=True)
        #print rmDirStatus
        #print type(rmDirStatus)
        printColor('green',path+'删除成功。')
        logger.info(path+'删除成功。')
        return 0
    except subprocess.CalledProcessError,msg:
        printColor('red','失败！原因：'+msg)
        logger.error('失败！原因：'+msg)
        return 1

#遍历部署环境变量函数
def mapDeployDict(dicts):
    printColor('green','^^^^^^^当前的部署环境^^^^^^^^^')
    for key,vaule  in dicts.items():
        printColor('green','%s:%s'%(key,vaule))
    printColor('green','###########################################')

#更换部署环境变量函数
def changeEnvironment():
    deployDict['userName']=changeUser()
    deployDict['passwd']=changePasswd()
    deployDict['localServicePath']=changeLocalServicePath()
    deployDict['localWebPath']=changeLocalWebPath()
    deployDict['remoteTarPath']=changeRemoteTarPath()
    deployDict['remoteScriptPath']=changeRemoteScriptPath()
    deployDict['shellScriptFile']=changeShellScript()

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

#service 菜单
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

#使用scp传输文件函数
def scpWork(localPath,username,host,remotePath,filename):
    #把项目 tar.gz包发送到目标主机上
    scp_NewKeys='.*(yes/no).*'
    scp_passwd='.*assword.*'
    scp_NoFile='No such.*'
    scpTarCmd='scp %s %s@%s:%s' %(localPath+filename,username,host,remotePath)
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
        return 0
    except paramiko.AuthenticationException,msg:
        printColor('green',msg)
        logger.error(msg)
        return 1
    except socket.error,msg:
        printColor('green',msg)
        logger.error(msg)
        return 1
    except IOError,msg:
        printColor('green',msg)
        logger.error(msg)
        return 1

#执行shell命令
def shellCmd(cmd):
    try:
        cmdStatus=subprocess.check_call(cmd,shell=True)
        #print cmdStatus
        #print type(cmdStatus)
        printColor('green','############执行成功.')
        logger.info('############执行成功.')
        return  0
    except subprocess.CalledProcessError,msg:
        printColor('red','失败！原因：'+msg)
        logger.error('失败！原因：'+msg)
        return 1




#部署主体函数，完成清理文件夹，git 项目 打包
def deployServiceWork(username,passwd,localServicePath,remoteTarPath,remoteScriptPath,version,policy,host,projectName,shellScriptFile):
    try:
        printColor('yellow','############开始部署任务')
        logger.info('############开始部署任务')
        #删除遗留的项目文件夹，并判断删除结果
        printColor('yellow','############step 1：删除当前路径下的'+projectName)
        logger.info('############step 1：删除当前路径下的'+projectName)
        rmDirPath='%s%s' %(localServicePath,projectName)
        rmStatus=rmDir(rmDirPath)
        if rmStatus==0:
            printColor('yellow','############step 2:在gitlab下载'+projectName+'项目包.')
            logger.info('############step 2:在gitlab下载'+projectName+'项目包.')
            #从gitlab把项目的工程打包下来，并判断打包是否成功
            gitCloneCmd='git clone -b '+version+' http://readonly:readonly@gitlab.xiniunet.com/xiniunet/'+projectName+'.git '+localServicePath+projectName
            shellStatus=shellCmd(gitCloneCmd)
            if shellStatus==0:
                printColor('yellow','############setp 3:进入'+projectName+'-contract/'+'子目录.')
                logger.info('############setp 3:进入'+projectName+'-contract/'+'子目录.')
                #进入项目的contract目录下先清理后deploy，并判断是否成功
                inFounfationContractCmd=localServicePath+projectName+'/'+projectName+'-contract/'
                os.chdir(inFounfationContractCmd)
                printColor('yellow','############step 4:'+projectName+'项目清理&部署.')
                logger.info('############step 4:'+projectName+'项目清理&部署.')
                mvnCleanCmd='mvn clean deploy'
                shellStatus=shellCmd(mvnCleanCmd)
                if shellStatus==0:
                    #进入项目的business目录下，打包项目，并判断是否成功
                    printColor('yellow','############step 5:进入'+projectName+'-business/'+'子目录.')
                    logger.info('############step 5:进入'+projectName+'-business/'+'子目录.')
                    inFounfationBusinessCmd=localServicePath+projectName+'/'+projectName+'-business/'
                    os.chdir(inFounfationBusinessCmd)
                    printColor('yellow','############step 6:'+projectName+'项目打包.')
                    logger.info('############step 6:'+projectName+'项目打包.')
                    mvnInstallCmd='mvn clean install -Dmaven.test.skip=true -U'
                    shellStatus=shellCmd(mvnInstallCmd)
                    if shellStatus==0:
                        printColor('yellow','############step 7:上传'+projectName+'项目包到远端服务器。')
                        logger.info('############step 7:上传'+projectName+'项目包到远端服务器。')
                        localPath='%s%s/%s-business/target/' %(localServicePath,projectName,projectName)
                        tarFilename='%s-business-%s-%s-assembly.tar.gz' %(projectName,version,policy)
                        shellStatus=putFileWork(localPath,username,passwd,host,remoteTarPath,tarFilename)
                        if shellStatus==0:
                            printColor('yellow','############step 8:上传'+shellScriptFile+'执行脚本到远端服务器。')
                            logger.info('############step 8:上传'+shellScriptFile+'执行脚本到远端服务器。')
                            shellStatus=putFileWork(localServicePath,username,passwd,host,remoteScriptPath,shellScriptFile)
                            if shellStatus==0:
                                return 0
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
        logger.error(msg)
        return 1
    except OSError,msg:
        printColor('red',msg)
        logger.error(msg)
        return 1
    except Exception,msg:
        printColor('red',msg)
        logger.error(msg)
        return 1
    except:
        printColor('red',projectName+'部署主体部分出现异常。')
        logger.error(projectName+'部署主体部分出现异常。')
        return 1


#定义log日志
def loger():
    logger=logging.getLogger('deployLogger')
    logger.setLevel(logging.DEBUG)
    fh=logging.FileHandler('xiniu-deploy.log',mode='w')
    fh.setLevel(logging.DEBUG)

    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s ')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

#main
def main():
    bigMenu()
    serviceMenu()
    for key,value in menuList.items():
        printColor('green',key+'模块：')
        version=value[0]
        policy=value[1]
        host=value[2]
        printColor('green','发布版本号：%s' %version)
        printColor('green','发布版本类型：%s' %policy)
        printColor('green','远端服务器地址：%s' %host)
        status=deployServiceWork(deployDict['userName'],deployDict['passwd'],deployDict['localServicePath'],deployDict['remoteTarPath'],deployDict['remoteScriptPath'],version,policy,host,key,deployDict['shellScriptFile'])
        if status==0:
            printColor('green',key+'ok')
            logger.info(key+'ok')
        else:
            printColor('red',key+'fail')
            logger.error(key+'fail')

if __name__=="__main__":
    logger=loger()
    mapDeployDict(deployDict)
    flag=rawInputColor('green','是否需要更改当前的部署环境Yes/no？')
    flag=flag.lower()
    print  flag
    if flag.strip()=='':
        flag='no'
    if flag=='yes'or flag=='y':
        changeEnvironment()
    mapDeployDict(deployDict)
    main()


