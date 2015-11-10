#!/usr/bin/env python
#coding=utf-8
#filename:initHost
#used：for vm kelong system to update ip,hostname hosts
__author__ = 'vzer'

import os
import string
import commands
import subprocess
import datetime
import socket
import re
import getpass
import logging

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


#look the ip address is ok
def checkIp(ipaddr):
    addr = ipaddr.strip().split('.')
    if len(addr) != 4:
        return False
    for i in range(4):
        if addr[i] == "":
            return False
        if not addr[i].isdigit():
            return False
        num = string.atoi(addr[i])
        if num <= 255 and num >= 0:
            continue
        else:
            return False
        i += 1
    return True



def inputIp():
    ipAddress=rawInputColor('green','enter the ip address(as:0.0.0.0):')
    while True:
        flag=checkIp(ipAddress)
        if flag:
            break
        else:
            ipAddress=rawInputColor('green','the ip address is not ok,please input again（as:0.0.0.0）：')
    return  ipAddress

def inputGatewayIp():
    ipAddress=rawInputColor('green','enter the gateway ip(as:0.0.0.0):')
    while True:
        flag=checkIp(ipAddress)
        if flag:
            break
        else:
            ipAddress=rawInputColor('green','the ip address is not ok,please input again（as:0.0.0.0）：')
    return  ipAddress


def inputHostName():
    hostName=rawInputColor('green','enter the hostname for the new system:')
    return hostName

def inputSimpleHostName():
    simpleHostName=rawInputColor('green','enter the simple hostname for the hosts file:')
    return simpleHostName

def inputMessage():
    ipAddress=inputIp()
    gateWayIp=inputGatewayIp()
    hostName=inputHostName()
    simpleHostName=inputSimpleHostName()
    while True:
        printColor('green','--------the ip:%s'
                           '--------the gateway:%s'
                           '-------the hostname:%s'
                           ' --------the simpleHostName:%s'%(ipAddress,gateWayIp,hostName,simpleHostName))
        flag=rawInputColor('green','do you want use?(y/n):')
        flag=flag.lower()
        if flag=='y'or flag=='yes':
            return (ipAddress,gateWayIp,hostName,simpleHostName)
        elif flag=='n' or flag=='no':
            ipAddress=inputIp()
            gateWayIp=inputGatewayIp()
            hostName=inputHostName()
            simpleHostName=inputSimpleHostName()
        else:
            flag=rawInputColor('red','please enter (y/yes or n/no):')



def shellCmd(cmd):
    try:
        cmdStatus=subprocess.check_call(cmd,shell=True)
        return  0
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
        return 1



def rmNetworkFIle():
    rmCmd='rm -rf /etc/udev/rules.d/70-persistent-net.rules'
    try:
        shellCmd(rmCmd)
    except Exception,msg:
        printColor('red',msg)

def changeHostName(hostName):
    sedCmd='''sed -i s'/HOSTNAME=.*/HOSTNAME=%s/g' /etc/sysconfig/network'''%hostName
    try:
        shellCmd(sedCmd)
    except Exception,msg:
        printColor('red',msg)

def changeIP(ipAddress,gatewayIP):
    sedCmd1='''sed -i s'/^IPADDR=.*/IPADDR=%s/g' /etc/sysconfig/network-scripts/ifcfg-eth0 ''' %ipAddress
    sedCmd2='''sed -i '/^UUID=.*/d' /etc/sysconfig/network-scripts/ifcfg-eth0 '''
    sedCmd3='''sed -i '/^HWADDR=.*/d' /etc/sysconfig/network-scripts/ifcfg-eth0 '''
    sedCmd4='''sed -i s'/^GATEWAY=.*/GATEWAY=%s/g' /etc/sysconfig/network-scripts/ifcfg-eth0 ''' %gatewayIP
    try:
        shellCmd(sedCmd1)
        shellCmd(sedCmd2)
        shellCmd(sedCmd3)
        shellCmd(sedCmd4)
    except Exception,msg:
        printColor('red',msg)

def changeHosts(hostName,ipAddress,simpleHostName):
    sedCmd='''sed -i s'/127.0.0.1/127.0.0.1 %s/g' /etc/hosts'''%hostName
    echoCmd='''echo '%s %s %s'>>/etc/hosts'''%(ipAddress,hostName,simpleHostName)
    try:
        shellCmd(sedCmd)
        shellCmd(echoCmd)
    except Exception,msg:
        printColor('red',msg)

def main():
    try:
        ipAddress,gatewayIp,hostName,simpleHostName=inputMessage()
        rmNetworkFIle()
        changeIP(ipAddress,gatewayIp)
        changeHostName(hostName)
        changeHosts(hostName,ipAddress,simpleHostName)
        shellCmd('reboot')
    except Exception,msg:
        printColor('red',msg)

if __name__=="__main__":
    main()
