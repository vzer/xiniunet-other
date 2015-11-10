#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#used:test the sqlalchemy modlues
__author__ = 'vzer'

from sqlalchemy import *
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker

engine=create_engine(
    'mysql+mysqldb://vzer:wwwlin123@192.168.1.246:3306/hosts?charset=utf8',
    echo=True
)

Base=declarative_base()

class ServerInfo(Base):
    __tablename__='serverinfo'
    id=Column(Integer,primary_key=True,autoincrement=True)
    hostname=Column(String(50))
    ip=Column(String(50))
    account=Column(String(50))
    password=Column(String(50))
    servicename=Column(String(50))


metadate=Base.metadata

if __name__=="__main__":
    metadate.create_all(engine)