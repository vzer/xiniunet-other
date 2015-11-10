#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'


import  MySQLdb
import string
import pxssh
import  re
dbName='monitorLog'

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

#初始化数据库monitorLog
def initDatebase(datebase='default'):
    try:
        conn=MySQLdb.connect(
        host='192.168.1.246',
        user='vzer',
        passwd='wwwlin123',
        port=3306
        )
        cur=conn.cursor()
        cur.execute('create database if not exists %s'%datebase)
        conn.select_db(datebase)
        cur.execute(
            '''CREATE TABLE `serverip` (
                    `id` int(8) NOT NULL auto_increment,
                    `style` varchar(255) DEFAULT NULL,
                    `hostname` varchar(255) DEFAULT NULL,
                    `ipaddress` varchar(255) DEFAULT NULL,
                     `module` varchar(255) DEFAULT NULL,
                    `environment` int(8) DEFAULT NULL,
                      PRIMARY KEY (`id`)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8;'''
        )
        cur.execute(
            '''
            CREATE TABLE `environmentvalue` (
  `id` int(11) NOT NULL,
  `environmentvalue` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of environmentvalue
-- ----------------------------
INSERT INTO `environmentvalue` VALUES ('1', 'develop');
INSERT INTO `environmentvalue` VALUES ('2', 'daily');
INSERT INTO `environmentvalue` VALUES ('3', 'test');
INSERT INTO `environmentvalue` VALUES ('4', 'Production');
INSERT INTO `environmentvalue` VALUES ('5', 'beforehand');'''
        )
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.MySQLError,e:
        print e



def insertValue(sytle,hostname,ipaddress,module,environment):
    try:
        conn=MySQLdb.connect(
            host='192.168.1.246',
            user='vzer',
            passwd='wwwlin123',
            port=3306
        )
        conn.select_db('monitorLog')
        cur=conn.cursor()
        cur.execute('insert into serverip(style,hostname,ipaddress,module,environment) values(%s,%s,%s,%s,%s)',(sytle,hostname,ipaddress,module,environment))
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.MySQLError,e:
        print e

#初始化服务环境值
def queryMysql():
    environmentValue={}
    try:
        conn=MySQLdb.connect(
            host='192.168.1.246',
            user='vzer',
            passwd='wwwlin123',
            port=3306
        )
        conn.select_db(dbName)
        cur=conn.cursor()
        count=cur.execute('select * from environmentvalue')
        result=cur.fetchmany(count)
        conn.commit()
        cur.close()
        conn.close()
        for id,value in result:
            print '%s %s'%(id,value)
            environmentValue['%s'%id]=value
        print environmentValue
    except MySQLdb.MySQLError,e:
        print e

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
    ipAddress=rawInputColor('green','Please enter the server ip address（refer0.0.0.0）：')
    while True:
        flag=checkIp(ipAddress)
        print  flag
        if flag:
            break
        else:
            ipAddress=rawInputColor('green','Ip address is not fit ，Please enter again（refer0.0.0.0）：')
    return  ipAddress

def pxsshWork(hostname,username,password,cmd):
    try:
        sshClient=pxssh.pxssh()
        sshClient.login (hostname, username, password, original_prompt='[$#>]')
        sshClient.sendline (cmd)
        sshClient.prompt()
        result=sshClient.before
        sshClient.logout()
        return result
    except pxssh.ExceptionPxssh,msg:
        printColor('red','login failed')
        printColor('red',str(msg))
        return False
    except Exception,msg:
        printColor('red','not kown error')
        printColor('red',str(msg))
        return  False


def menu():
    try:
        while True:
            choice=rawInputColor('green','1-Develop,2-Daily,3-Test,4-Production,5-Deforehand:')
            if choice=='1':
               smallMenu(1)
            elif choice=='2':
                smallMenu(2)
            elif choice=='3':
                smallMenu(3)
            elif choice=='4':
                smallMenu(4)
            elif choice=='5':
                smallMenu(5)
            else:
                choice=rawInputColor('green','1-develop,2-daily,3-test,4-Production,5-deforehand:')
            choice=rawInputColor('green','Do you want add continue:(yes/no)')
            choice=choice.lower()
            if choice=='no' or choice=='n':
                break
    except Exception,e:
        printColor('yellow','no know error!!')





def smallMenu(choice1):
    try:
        while True:
            choice2=rawInputColor('green','1-Service,2-Web,3-Other:')
            if choice2=='1':
                number=rawInputColor('green','1-Foundation，2-Distribution，3-Marketplace，4-Backend:')
                if number=='1':
                    process(choice1,'Foundation','Service')
                elif number=='2':
                    process(choice1,'Distribution','Service')
                elif number=='3':
                    process(choice1,'Distribution','Service')
                elif number=='4':
                    process(choice1,'Distribution','Service')
                else:
                    print 'no know error'
            elif choice2=='2':
                number=rawInputColor('green','1-Foundation，2-Distribution，3-Marketplace，4-Backend:')
                if number=='1':
                    process(choice1,'Foundation','Web')
                elif number=='2':
                    process(choice1,'Distribution','Web')
                elif number=='3':
                    process(choice1,'Distribution','Web')
                elif number=='4':
                    process(choice1,'Distribution','Web')
                else:
                    print 'no know error'
            elif choice2=='3':
                number=rawInputColor('green','1-Foundation，2-Distribution，3-Marketplace，4-Backend:1')
                if number=='1':
                    process(choice1,'Foundation','Other')
                elif number=='2':
                    process(choice1,'Distribution','Other')
                elif number=='3':
                    process(choice1,'Distribution','Other')
                elif number=='4':
                    process(choice1,'Distribution','Other')
                else:
                    print 'no know error'
            else:
                print 'no know error'
            choice=rawInputColor('green','Do you want add continue:(yes/no)')
            choice=choice.lower()
            if choice=='no' or choice=='n':
                break

    except Exception,e:
        print  e


def process(environment,style,module):
    try:
        password='root@xiniu'
        username='root'
        while True:
            ipaddress=inputIp()
            print ipaddress
            cmd='hostname'
            result=pxsshWork(ipaddress,username,password,cmd)
            if result:
                regex=re.compile('hostname\r\n(.*)\r\n').findall(result)
                insertValue(style,''.join(regex),ipaddress,module,environment)
            choice=rawInputColor('green','Do you want add continue:(yes/no)')
            choice=choice.lower()
            if choice=='no' or choice=='n':
                break
    except Exception,e:
        print e




def main():
    try:
        conn=MySQLdb.connect(
            host='192.168.1.246',
            user='vzer',
            db =dbName,
            passwd='wwwlin123',
            port=3306
        )
        menu()
    except MySQLdb.MySQLError,e:
        initDatebase(dbName)



if __name__=="__main__":
    main()