#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import datetime
import elasticsearch
from
es=elasticsearch.Elasticsearch('192.168.1.235:9200')
#print es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.datetime.now()})
print es.get(index="flume-nginx-2015-04-18",id='AUzJ29UtOIwJ7XsjaxQs')
#for i in range(3000):
    #res=es.index(index='ceshi',doc_type='vzer',body={'name':i,'time':datetime.datetime.now()},id=i)
    #print i
