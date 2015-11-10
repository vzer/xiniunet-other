#!/usr/bin/env python
#coding=utf-8
#kafka-python clients
__author__ = 'vzer'

from pykafka.balancedconsumer import BalancedConsumer
from pykafka.client import KafkaClient
from pykafka.topic import Topic
from pykafka.cluster import Cluster
from pykafka.handlers import Handler
client=KafkaClient(hosts='192.168.1.244:9092')
topic=client.topics['lei']
#comsumer=topic.get_balanced_consumer(consumer_group='consumer-group',auto_commit_enable=True,zookeeper_connect='192.168.1.245:2181')
comsumer=topic.get_simple_consumer()
for

