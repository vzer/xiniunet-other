#!/usr/bin/env python
# _*_ coding:utf8 _*_
__author__ = 'vzer'

import os
import string
import re
import datetime
import subprocess
import sys
import socket
import time
import pxssh
from sqlalchemy import *
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
import web
from web.contrib.template import render_jinja

urls=(
    '/index','Index',
    '/add','Add',
    '/view','View'
)




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

def main(start,stop):
    for ip in xrange(start,stop):
        (status,result)=shellCmd('fping 192.168.1.%s'%ip)
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


#sql
engine=create_engine(
    'mysql+mysqldb://vzer:wwwlin123@192.168.1.246:3306/hosts?charset=utf8',
    echo=True
)
DBsession=sessionmaker(bind=engine)
Base=declarative_base()

class ServerInfo(Base):
    __tablename__='serverinfo'
    id=Column(Integer,primary_key=True,autoincrement=True)
    hostname=Column(String(50))
    ip=Column(String(50))
    account=Column(String(50))
    password=Column(String(50))
    servicename=Column(String(50))


metadate=Base.metadata


#web
app=web.application(urls,locals())
session=web.session.Session(app,web.session.DiskStore('session'))
render=render_jinja('templates',encoding='utf-8')
ksession=DBsession()
#page
class Index:
    def GET(self):
        all_list=ksession.query(ServerInfo).order_by(ServerInfo.id.desc()).all()
        return render.index(all_list=all_list)

class Add:
    def GET(self):
        return render.add()
    def POST(self):
        postdata=web.input()
        start=web.net.websafe(postdata.start)
        stop=web.net.websafe(postdata.stop)
        #main(int(start),int(stop))
        raise web.seeother('/index')
        return u'任务已经添加'


class View:
    def GET(self):
        status=getStatus()
        return status


if __name__=="__main__":
    app.run()
