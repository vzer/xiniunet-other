#!/usr/bin/env python
#coding=utf-8
#kafka-python clients
__author__ = 'vzer'
import sys
import os
import re
from pykafka.client import KafkaClient
from pykafka.simpleconsumer import SimpleConsumer
import pykafka.topic
from datetime import datetime
from pykafka.cluster import Cluster
from elasticsearch import Elasticsearch
import ConfigParser
import time




#连接kafka
def linkKafka():
    client=KafkaClient(hosts='192.16.1.244:9092')
    topic=client.topics['xiniunet']
    return topic

def linkElasticsearch():
    es=Elasticsearch(hosts='192.168.1.235:9200')
    return es

def matchData(line):
    doc={}
    matchs=line.split('|')
    if len(matchs)==12:
        field={
            'level':matchs[1],
            'ip':matchs[2],
            'thread':matchs[4],
            'class':matchs[5],
            'tenantId':matchs[6],
            'userId':matchs[7],
            'module':matchs[9],
            'system':matchs[10],
            'message':matchs[11]

        }
    doc={"field":field,"time":matchs[0]}
    return doc



def processData():
    topic=linkKafka()
    es=linkElasticsearch()
    consumer=topic.get_simple_consumer()
    try:
        for message in consumer:
            if message is not None:
                doc=matchData(message.value)
                if doc:
                    print message.offset,doc
                    index='xiniulog-'+time.strftime('%Y-%m-%d')
                    res=es.index(index=index,doc_type='string',id=int(message.offset),body=doc)
                    kkk=es.index()
    except Exception,msg:
        print msg


def read_config(config_file_path, field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result

def write_config(config_file_path, field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except:
        print 11
        sys.exit(1)
    return True

if __name__=="__main__":
    processData()
