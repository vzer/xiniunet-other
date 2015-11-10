#!/usr/bin/env python
# _*_ coding:utf8 _*_
__author__ = 'vzer'

import  multiprocessing
import  proxy
import os

class web(object):
    def __init__(self):
        self._cntl_q=cntl_q
        self._data_q=data_q
        self._send=send
        print '-----web-cntl ,data--------'
        print self._cntl_q
        print self._data_q
        print self._send


    def put(self):
        while True:
            print 'current pid is :%s'%os.getpid()
            event=raw_input('enter:cntl')
            data=raw_input('enter:data')
            self._cntl_q.put({'event':event})
            self._data_q.put({'data':data})
            print 'put ok'
            raw_input('continue:\n')



if __name__ == '__main__':
    cntl_q=multiprocessing.Queue()
    data_q=multiprocessing.Queue()
    (send,resv)=multiprocessing.Pipe()
    print '-----main-cntl ,data--------'
    print cntl_q
    print data_q
    print send
    print resv
    proc=multiprocessing.Process(target=proxy.proxy,args=(cntl_q,data_q,resv))
    proc.start()
    web=web()
    web.put()

