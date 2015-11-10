#!/usr/bin/env python
#coding=utf-8
#filename:delete the ElasticSearch Index
#used：auto delete the elasticsearch index in order the time
__author__ = 'vzer'
import  datetime
import subprocess
import smtplib
from email.mime.text import MIMEText

mailto_list=['zhangcunlei@xiniunet.com ']
mail_host="mail.xiniunet.com"
mail_user="zhangcunlei@xiniunet.com"
mail_pass="wwwlin123"
mail_postfix="xiniunet.com"
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

def send_mail(to_list,sub,content):
    me="ElasticSearch-Mail"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


def shellCmd(index,cmd):
    try:
        output=subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
        printColor('green','date:%s delete status---->%s'%(index,output))
        return  output
    except subprocess.CalledProcessError,msg:
        printColor('red',msg)
        return msg

def main():
    context=''
    printColor('yellow','-----------------------%s delete result-----------------------'%datetime.datetime.now().strftime('%Y.%m.%d'))
    context =context+'-----------------------%s delete result-----------------------' % datetime.datetime.now().strftime('%Y.%m.%d')+'\n'
    printColor('green','----------------------------------------------------------------')
    context=context+'   ----------------------------------------------------------------\n'
    for i in range(7):
        now_time = datetime.datetime.now()
        days=datetime.timedelta(days=i+3)
        index=(now_time-days).strftime('%Y.%m.%d')
        deleteCmd='''curl -s -XDELETE 'http://10.117.210.89:9200/*-%s' '''%index
        output=shellCmd(index,deleteCmd)
        context=context+'   date:%s delete status---->%s\n'%(index,output)
        printColor('green','----------------------------------------------------------------')
        context=context+'-------------------------------------------------------------------------\n'
    return context



if __name__=="__main__":
    context=main()
    if send_mail(mailto_list,"%s Delete Elastic Index status"%datetime.datetime.now().strftime('%Y.%m.%d'),context):
        print "发送成功"
    else:
        print "发送失败"


