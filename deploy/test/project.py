#!/usr/bin/env python
#coding=utf8
__author__ = 'vzer'

class TT(object):
    fen=0

class T(TT):
    def __init__(self):
        self._name='name'
        self._id=111
    __slots__='_name','_id'

class X(object):
    def __init__(self):
        self._name='name'
        self._id=111
    __slots__='_name','_id'


if __name__ == '__main__':
    t=T()
    x=X()
    print t.__dict__
    print T.__dict__
    print TT.__dict__
