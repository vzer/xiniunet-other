#!/usr/bin/env python
#/coding=utf-8
#测试raw_input
__author__ = 'vzer'
import subprocess
import re
import  getpass

deployDict={}
deployDict['userName']='root'
deployDict['passwd']='root@xiniu'
deployDict['remoteTarPath']='/xiniu/updateapps/'
deployDict['remoteScriptPath']='/xiniu/scripts/'
deployDict['localServicePath']='/vzer/service/'
deployDict['localWebPath']='/vzer/web/'
deployDict['shellScriptFile']='webdeploy.sh'


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
        iText = '\033[1;33;40m%s\033[0m'
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

#定义创建本地目录函数
def makeDir(path):
    mkdirCmd='mkdir -p '+path
    mkdirStatus=subprocess.check_call(mkdirCmd,shell=True)
    if int(mkdirStatus)==0:
        return True
    else:
        return False

#遍历部署环境变量函数
def mapDeployDict(dicts):
    printColor('green','^^^^^^^当前的部署环境^^^^^^^^^')
    for key,vaule  in dicts.items():
        printColor('green','%s:%s'%(key,vaule))

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
    while not re.search('\d\.\d\.\d',version):
        version=rawInputColor('green','输入的格式错误（参照：2.1.0）：')
    return version

#定义发布版本类型函数
def inputPolicy():
    number=rawInputColor('green','请选择发布版本类型1-SNAPSHOT, 2-RELEASE（默认：SNAPSHOT）：')
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

if __name__=="__main__":
    mapDeployDict(deployDict)
    flag=rawInputColor('green','是否需要更改当前的部署环境Yes/no？')
    flag=flag.lower()
    if flag.strip()=='':
        flag='no'
    if flag=='yes'or flag=='y':
        changeEnvironment()
    mapDeployDict(deployDict)
    #mkdirStatus=makeDir(deployDict['localServicePath'])
