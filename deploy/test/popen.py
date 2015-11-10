#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import subprocess
import sys


def shellCmd(cmd):
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    (processStdout,processStderr) = process.communicate()
    retcode = process.poll()
    if retcode:
        if cmd is None:
            cmd ='no commands.'
        raise subprocess.CalledProcessError(returncode=retcode,cmd=cmd)
    return (retcode,processStdout)

if __name__=="__main__":
    try:
        while True:
            cmd=raw_input('enter command(q/quit):')
            (status,result)=shell(cmd)
            print 'status:%s'%status
            print 'status:%s'%result
            if cmd=='q' or cmd=='quit':
                break
    except subprocess.CalledProcessError,msg:
        print msg