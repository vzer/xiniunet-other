#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import  redis

rc=redis.Redis(host='192.168.1.240',port=6379,db=0)
ip_addr='192.168.1.100'
count=rc.lpush('192.168.1.100',10)
rc.publish('count_alarm',count)
rc.publish('ip_alarm',ip_addr)
