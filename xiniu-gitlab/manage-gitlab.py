#!/usr/bin/env python
# _*_coding:utf8 _*_
__author__ = 'vzer'

import gitlab
from sqlalchemy import *
from sqlalchemy.orm import scoped_session,sessionmaker
import models

# create_engine(数据库://用户名:密码(没有密码则为空)@主机名:端口/数据库名',echo =True)
MYSQL_DB = "deploy"
MYSQL_USER = "vzer"
MYSQL_PASS = "wwwlin123"
MYSQL_HOST = "192.168.1.246"
MYSQL_PORT = int("3306")

engine=create_engine(
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8'%
    (MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT,MYSQL_DB),
    echo=False
)

#pack组件数据库链接session
DBsession=scoped_session(sessionmaker(bind=engine))



git2=gitlab.Gitlab("http://192.168.20.100")
git2.login('xiniunet','root@xiniu')
#############################################
git1=gitlab.Gitlab("http://192.168.1.102")
git1.login('xiniunet','root@xiniu')
################################################
git3=gitlab.Gitlab("http://192.168.3.100")
git3.login('xiniunet','root@xiniu')

################################################
git4=gitlab.Gitlab("http://192.168.4.100")
git4.login('xiniunet','root@xiniu')



def addGit_url(git):
    for item in git.getprojects(per_page=200):

        ids=DBsession.query(models.Models).filter(models.Models.mode_name==item["name"],models.Models.type_id=="10002").all()
        #print item["id"],item["name"]
        if ids:
            for k in  ids:

                info=models.Models(model_id=k.model_id,mode_name=k.mode_name,git_url=item["http_url_to_repo"])
                DBsession.merge(info)
                print info.model_id,info.mode_name,info.git_url
                DBsession.commit()

def addUserToProject(git,projectName,userName):
    try:
        for project in git.getprojects(per_page=200):
            if project["name"]==projectName:
                pro_id=project["id"]
        for user in git.getusers(per_page=200):
            if user["name"]==userName:
                user_id=user["id"]
        git.addprojectmember(project_id=pro_id,user_id=user_id,access_level=30)
    except UnboundLocalError,msg:
        print UnboundLocalError,msg




if __name__ == '__main__':
  addUserToProject(git1,projectName="product1",userName=u"罗海峰")