#!/usr/bin/env python
#coding=utf-8
#filename:deploy.py
__author__ = 'vzer'

import sys
import os
import string
import commands
import subprocess
import datetime
import socket
import re
import getpass
import logging

#定义log日志
def loger():
    logger=logging.getLogger('deployLogger')
    logger.setLevel(logging.DEBUG)
    fh=logging.FileHandler('xiniu-deploy.log',mode='w')
    fh.setLevel(logging.DEBUG)

    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s ')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

if __name__=="__main__":
    logger=loger()
    for i in range(10000):
        logger.info('loadbance test current is %s' %i)