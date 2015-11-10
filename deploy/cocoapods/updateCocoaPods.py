#!/usr/bin/env python
#coding=utf-8
#filename:updateCocoaPods.py
#use: xiugai github cococapods to xiniunet
__author__ = 'vzer'

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import subprocess
import json
import pxssh
import time
import getpass

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

#远程ssh模块
def pxsshWork(hostname,username,password,cmd):
    try:
        sshClient=pxssh.pxssh()
        sshClient.login (hostname, username, password, original_prompt='[$#>]')
        sshClient.sendline(cmd)
        sshClient.prompt()
        printColor('green',"git-mirror进程是：")
        printColor('green',sshClient.before)
        sshClient.logout()
    except pxssh.ExceptionPxssh,e:
        print "login failed"
        print str(e)

#内部cocoapodsServer git 推送
def gitPush():
    printColor('yellow','-------------------------------------------------------------------------------------------------')
    os.chdir('/home/gitmirror/kks/xiniu-CocoaPods')
    gitaddCmd='git add -A'
    gitCommitCmd='git commit -m "add the cocoapods %s"'%targetDir
    gitPushCmd='git push -u origin master'
    try:
        subprocess.check_call(gitaddCmd,shell=True)
        subprocess.check_call(gitCommitCmd,shell=True)
        subprocess.check_call(gitPushCmd,shell=True)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)

#shell命令执行
def shellCmd(cmd):
    shellCmdStatus=-1
    try:
        shellCmdStatus=subprocess.check_call(cmd,shell=True)
    except UnboundLocalError,msg:
        printColor('red',msg)
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
    return shellCmdStatus


#git-mirror
def gitMirror(projectName,cmd,mirrorCount=3):
    count=1
    while True and count<=mirrorCount:
        printColor('yellow','-------------------------------------------------------------------------------------------------')
        printColor('green','第%s次镜像github组件：%s'%(count,projectName))
        gitCmdStatus=shellCmd(cmd)
        if gitCmdStatus!=0:
            printColor('red','%s组件镜像失败。准备执行%s组件更新检查.'%(projectName,projectName))
            updateCmd='/home/gitmirror/gitlab-mirrors/update_mirror.sh %s'%projectName
            updateCmdStatus=shellCmd(updateCmd)
            if updateCmdStatus!=0:
                printColor('red','%s组件更新失败,准备删除错误更新文件，重试.'%projectName)
                deleteMirrorCmd='/home/gitmirror/gitlab-mirrors/delete_mirror.sh --delete %s'%projectName
                rmFileStatus=shellCmd(deleteMirrorCmd)
            else:
                printColor('green','%s组件更新成功.'%projectName)
                break
        else:
            printColor('green','%s组件镜像成功.'%projectName)
            break
        count=count+1
    lsMirrorCmd='/home/gitmirror/gitlab-mirrors/ls-mirrors.sh'
    printColor('yellow','-------------------------------------------------------------------------------------------------')
    printColor('green','镜像成功的组件如下：')
    shellCmd(lsMirrorCmd)

def  main():
    try:
        targetDir=rawInputColor('green','输入需要下载的CocoaPods组件：')
        targetDir=targetDir.strip()
        cpCmd='cp -R %s%s %s'%(githubCocoaPath,targetDir,gitlabCocoaPath)
        cmdStatus=subprocess.check_call(cpCmd,shell=True)
    except subprocess.CalledProcessError:
        printColor('red','CocoaPods组件不存在，请检查输入，或联系管理员更新CocoaPods官方库。')
        exit()
    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent,dirnames,filenames in os.walk(gitlabCocoaPath+targetDir):
        for filename in filenames:
            if filename.endswith(".json"):
                readFile=open(os.path.join(parent,filename),'r')
                jsonCfg=json.load(readFile)
                readFile.close()
                try:
                    githubhttp=jsonCfg['source']['git']
                    printColor('yellow','-------------------------------------------------------------------------------------------------')
                    printColor('green',"当前处理的Json文件是:"+os.path.join(parent,filename))
                    if not (githubhttp in flag):
                        tag=jsonCfg['source']['tag']
                        flag.append(githubhttp)
                        gitCmd='/home/gitmirror/gitlab-mirrors/add_mirror.sh --git --project-name %s --mirror %s'%(targetDir+tag,githubhttp)
                        printColor('green',"git-mirror执行命令："+gitCmd)
                        gitMirror(projectName=targetDir+tag,cmd=gitCmd,mirrorCount=5)
                        #pxsshWork('192.168.1.201','gitmirror','wwwlin123',gitCmd)
                    gitlabHttp='http://cocoapods.xiniunet.com/mirrors/%s.git'%(targetDir.lower()+str(tag).replace('.','-'))
                    jsonCfg['source']['git']=gitlabHttp
                    printColor('red',"gitlab地址是："+jsonCfg['source']['git'])
                except KeyError:
                    githubhttp=jsonCfg['source']['svn']
                    printColor('green',"当前处理的Json文件是:"+os.path.join(parent,filename))
                    if not (githubhttp in flag):
                        tag=jsonCfg['source']['tag']
                        flag.append(githubhttp)
                        svnCmd='/home/gitmirror/gitlab-mirrors/add_mirror.sh --svn --project-name %s --mirror %s'%(targetDir+tag,githubhttp)
                        printColor('green',"git-mirror执行命令："+svnCmd)
                        gitMirror(projectName=targetDir+tag,cmd=svnCmd,mirrorCount=5)
                        #pxsshWork('192.168.1.201','gitmirror','wwwlin123',svnCmd)
                    gitlabHttp='http://cocoapods.xiniunet.com/mirrors/%s.git'%(targetDir.lower()+str(tag).replace('.','-'))
                    jsonCfg['source']['svn']=gitlabHttp
                    printColor('red',"gitlab地址是："+jsonCfg['source']['svn'])
                writeFile=open(os.path.join(parent,filename),'w')
                json.dump(jsonCfg,writeFile,sort_keys=True,indent=2)
                writeFile.close()
    gitPush()

#更新官方cocoapods版本库
def updateGithubCocoaPods():
    cmd='/home/gitmirror/gitlab-mirrors/update_mirror.sh  CocoaPods'
    cmdStatus=shellCmd(cmd=cmd)
    if cmdStatus!=0:
        printColor('red','更新失败，请重试。')
        exit()
    else:
        os.chdir('/home/gitmirror/kks/CocoaPods')
        cmdStatus=shellCmd('git pull origin master')
        if cmdStatus!=0:
            printColor('red','更新失败，请重试。')



 #更新单个单个Cocoapods组件
def updateCocoapodsComponents():
    return 0
 #更新git-mirror上所有组件
def updateGitMirror():
    rmCronFile='rm -rf /home/gitmirror/gitlab-mirrors/cron.log'
    cmd='/home/gitmirror/gitlab-mirrors/git-mirrors.sh'
    cmdStatus=shellCmd(cmd)
    if cmdStatus!=0:
        printColor('red','更新失败，请重试。')
    else:
        readFile=open('/home/gitmirror/gitlab-mirrors/cron.log',mode='r')
        for line in readFile:
            printColor('green',line,flag=True)
        readFile.close()


#菜单函数
def menu():
    printColor('green','欢迎使用Cocoapods服务维护系统')
    printColor('green','当前时间：%s   当前登录用户：%s'%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),getpass.getuser()))
    if getpass.getuser()!='gitmirror':
        printColor('red','请使用gitmirror用户登录，程序退出.')
        exit()
    printColor('green','1-更新官方Cocoapods版本库')
    printColor('green','2-更新单个Cocoapods组件')
    printColor('green','3-更新git-mirror上所有组件（耗时长！）')
    printColor('green','4-下载官方Cocoapods组件到本地Cocoapods')
    inputChoice=rawInputColor('blue','请输入选择（按q/quit退出）：')
    while True:
        inputChoice=inputChoice.lower()
        if inputChoice=='q' or inputChoice=='quit':
            exit()
        if inputChoice=='1':
            return 1
        elif inputChoice=='2':
            return 2
        elif inputChoice=='3':
            return 3
        elif inputChoice=='4':
            return 4
        else:
            inputChoice=rawInputColor('blue','输入错误，请重新输入（按q/quit退出）：')
            continue


if __name__=="__main__":
    global flag
    flag=[]
    githubCocoaPath='/home/gitmirror/kks/CocoaPods/Specs/'
    gitlabCocoaPath='/home/gitmirror/kks/xiniu-CocoaPods/Specs/'
    #main()
    #menu()
    updateGitMirror()










