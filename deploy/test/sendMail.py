#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import smtplib
from email.mime.text import MIMEText
mailto_list=['zhangcunlei@xiniunet.com ']
mail_host="mail.xiniunet.com"
mail_user="zhangcunlei@xiniunet.com"
mail_pass="wwwlin123"
mail_postfix="xiniunet.com"

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



if __name__ == '__main__':
    if send_mail(mailto_list,"你好","测试邮件\n 你好"):
        print "发送成功"
    else:
        print "发送失败"