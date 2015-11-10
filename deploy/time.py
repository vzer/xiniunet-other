#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import datetime
now_time = datetime.datetime.now()
yes_time = now_time -datetime.timedelta(days=2)
yes_time_nyr = yes_time.strftime('%Y%m%d')

print now_time

print  now_time.strftime('%Y-%m-%d')
print  yes_time_nyr