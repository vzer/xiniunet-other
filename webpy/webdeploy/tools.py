#!/usr/bin/env python
#coding=utf8
__author__ = 'vzer'

from setting import *
from models import *

if __name__ == '__main__':
    metadate=Base.metadata
    metadate.create_all(engine)