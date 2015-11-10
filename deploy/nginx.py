#!/usr/bin/env python
#coding=utf8
import os
import fileinput
import re
import sys
import os
import re

#日志的位置
nginxLog="""2015-05-14 14:36:37,194 | info | 192.168.1.124 | """
timeP=r"""?P<time>[\d\:\ \-\,]+"""
levelP = r"?P<level>[.]*"
ipP = r"?P<ip>[\d.]*"
threadP=r"?P<thread>[\w-\d]*"
classP=r"""?P<class>[\w.]*"""
number1P=r"?P<number1>\d*"
number2P=r"?P<number2>\d*"
moduleP=r"?P<module>\w*"
systemP=r"?P<system>\w*"
messageP=r"""?P<message>.*"""
'''
#以"开始, 除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?),#以"结束
#"http://test.myweb.com/myAction.do?method=view&mod_id=&id=1346"
referP = r"""?P<refer>\"[^\"]*\""""
#以"开始, 除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?),以"结束
#"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
userAgentP = r"""?P<userAgent>\"[^\"]*\""""
#以(开始, 除双引号以外的任意字符 防止匹配上下个()项目(也可以使用非贪婪匹配*?),以"结束
#(compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
userSystems = re.compile(r'\([^\(\)]*\)')
#以"开始，除双引号以外的任意字符防止匹配上下个""项目(也可以使用非贪婪匹配*?),以"结束
userlius = re.compile(r'[^\)]*\"')
#原理：主要通过空格和-来区分各不同项目，各项目内部写各自的匹配表达式
'''
kkk=nginxLog.split('|')
#nginxLogPattern = re.compile(r"(%s)\ | (%s)\ | (%s)\ | \ | (%s)\ | (%s)\ | (%s)\ | (%s)\ | \ | (%s)\ | (%s)\ | (%s)" %(timeP,levelP,ipP,threadP,classP,number1P,number2P,moduleP,systemP,messageP), re.VERBOSE)
nginxLogPattern = re.compile(r"""(%s) | (%s) | (%s) | """ %(timeP,levelP,ipP), re.VERBOSE)
def testNginx():
    matchs=nginxLogPattern.match(nginxLog)
    print matchs.groups()
    '''
    if matchs != None:
        allGroup = matchs.groups()
        time = allGroup[0]
        level = allGroup[1]
        ipadd = allGroup[2]
        thread = allGroup[3]
        classes = allGroup[4]
        number1 = allGroup[5]
        number2 = allGroup[6]
        module=allGroup[7]
        system=allGroup[8]
        #message=allGroup[9]
        #Time = time.replace('T',' ')[1:-7]
        print matchs.groups()

        if len(userAgent) > 20:
            userinfo = userAgent.split(' ')
            userkel =  userinfo[0]
            try:
                usersystem = userSystems.findall(userAgent)
                usersystem = usersystem[0]
                print usersystem
                userliu = userlius.findall(userAgent)
                value = [ip,Time,request,status,bodyBytesSent,refer,userkel,usersystem,userliu[1]]
                print value
            except IndexError:
                userinfo = userAgent
                value = [ip,Time,request,status,bodyBytesSent,refer,userinfo,"",""]
                print value
        else:
            useraa = userAgent
            value = [ip,Time,request,status,bodyBytesSent,refer,useraa,"",""]
            print value
        '''




if __name__ == "__main__":
    testNginx()
