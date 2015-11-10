#!/usr/bin/env python
#coding=utf-8
#作用 使用 sudo 删除文件夹
__author__ = 'vzer'

import subprocess

print('test ls')
trun_code=subprocess.call('ls -al',shell=True)
print trun_code
print'测试 sudo yum'
subprocess.call('sudo yum -y install lrzsz',shell=True)

