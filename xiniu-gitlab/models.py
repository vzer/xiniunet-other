#!/usr/bin/env python
#coding=utf8
#  use:for web deploy models
__author__ = 'vzer'


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base=declarative_base()

class ServerInfo(Base):
    __tablename__='serverinfo'
    id=Column(Integer,primary_key=True,autoincrement=True,unique=True)
    hostname=Column(String(50))
    ip=Column(String(50))
    account=Column(String(50))
    password=Column(String(50))
    servicename=Column(String(50))
    environment=Column(String(50))

class User(Base):
    __tablename__='user'
    id=Column(String(50),primary_key=True,unique=True)
    user_account=Column(String(50),unique=True)
    user_password=Column(String(50))
    email=Column(String(50),unique=True)
    nick_name=Column(String(50))
    isactive=Column(Boolean,default=False)
    isadmin=Column(Boolean,default=False)

class Permission_Group(Base):
    __tablename__='permission_group'
    id=Column(Integer,primary_key=True,autoincrement=True,unique=True)
    group_name=Column(String(50),unique=True)

class TaskLogs(Base):
    __tablename__='tasklog'
    id=Column(String(50),primary_key=True,unique=True)
    user_id=Column(String(50))
    family=Column(String(50))
    models=Column(String(50))
    version=Column(String(50))
    status=Column(String(50))
    failure_times=Column(Integer)
    logtime=Column(DateTime,default=datetime.datetime.now())
    context=Column(Text)

class DeployType(Base):
    __tablename__='deploytype'
    type_id=Column(String(50),primary_key=True,unique=True)
    type_name=Column(String(50),unique=True)

class Models(Base):
    __tablename__='models'
    model_id=Column(Integer,primary_key=True,autoincrement=True,unique=True)
    type_id=Column(String(50))
    type_name=Column(String(50))
    mode_name=Column(String(50))
    mode_pet=Column(String(50),unique=True)
    remote_path=Column(String(50))
    git_url=Column(String(50))


######################################################################################################################
#订单生成器
def createWorkOrder():
    try:
        workOrder=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return uuid.uuid3(uuid.NAMESPACE_DNS,workOrder)
    except Exception,msg:
        print str(msg)
