#!/usr/bin/env python
# _*_ coding:utf8 _*_
__author__ = 'vzer'

import os
import multiprocessing as mp
import time

def proc_worker(cntl_q,data_q):
    item=data_q.get()
    print os.getpid(),item
    time.sleep(3)
    cntl_q.put({'event': 'exit', 'pid': os.getpid()})



def proxy(cntl_q,data_q):
    proc_pool = {}
    print '-----proxy-cntl ,data--------'
    print cntl_q
    #print data_q

    while True:
        if not cntl_q.empty():
            item=cntl_q.get()
            if item['event'] == 'data':
                proc = mp.Process(target=proc_worker, args=(cntl_q, data_q))
                proc.start()
                proc_pool[proc.pid] = proc
                print 'worker {} started'.format(proc.pid)
            elif item['event'] == 'exit':
                proc = proc_pool.pop(item['pid'])
                proc.join()
                print 'child {} stopped'.format(item['pid'])
            else:
                print 'It\'s impossible !'