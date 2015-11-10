#!/usr/bin/env python
#coding=utf8
# use:for web deploy setting
__author__ = 'vzer'

from sqlalchemy import *
from sqlalchemy.orm import scoped_session,sessionmaker
import web
from web.contrib.template import render_jinja
import multiprocessing

#jinja
render=render_jinja('templates',encoding='utf-8')
cntl_q=multiprocessing.Queue()
data_q=multiprocessing.Queue()

# create_engine(数据库://用户名:密码(没有密码则为空)@主机名:端口/数据库名',echo =True)
MYSQL_DB = "deploy"
MYSQL_USER = "vzer"
MYSQL_PASS = "wwwlin123"
MYSQL_HOST = "192.168.1.246"
MYSQL_PORT = int("3306")

engine=create_engine(
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8'%
    (MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT,MYSQL_DB),
    echo=True
)

#pack组件数据库链接session
DBsession=scoped_session(sessionmaker(bind=engine))

#网站主体数据库链接session
def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
