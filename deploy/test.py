#!/usr/bin/env python
#coding=UTF-8
__author__ = 'vzer'

import  os
import time

testString='  kks   '
print testString.strip()
'''
a=[[1,2],[4,5]]
print a
b=[]
b=a[0]
a[0]=a[1]
a[1]=b
print a
'''

b=[[1,2],[3,4]]
b[0]=b[0]^b[1]
b[1]=b[0]^b[1]
b[0]=b[0]^b[1]

print b


for i in b:
    print i



