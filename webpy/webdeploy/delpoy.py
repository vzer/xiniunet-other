#!/usr/bin/env python
# _*_ coding:utf8 _*_
__author__ = 'vzer'

import web
from setting import render
from setting import load_sqla,cntl_q,data_q
import models
import multiprocessing as mp
import pack
import sys
reload(sys)
sys.setdefaultencoding('utf8')

urls=(
    '/index','Index',
    '/add/(.*)','Add',
    '/view/(.*)','View'
)

#web
app=web.application(urls,locals())
app.add_processor(load_sqla)
sesssion=web.session.Session(app,web.session.DiskStore('session'))

class Index:
    def GET(self):
        return u'no'

class Add(object):
    def __init__(self):
        self._workOrder=str(models.createWorkOrder())

    def GET(self,deployType):
        workOrder=self._workOrder
        if len(deployType)!=0:
            modelMap=web.ctx.orm.query(models.Models).filter(models.Models.deploy_type==deployType).order_by(models.Models.model_id.desc()).all()
        else:
            modelMap=web.ctx.orm.query(models.Models).order_by(models.Models.model_id.desc()).all()
        return render.add(workorder=workOrder,modelmap=modelMap)

    def POST(self,deployType):
        postdata=web.input()
        workOrder=self._workOrder
        modelPet=web.net.websafe(postdata.models)
        versionNumber=web.net.websafe(postdata.version_number)
        sql_list=web.ctx.orm.query(models.Models).filter(models.Models.mode_pet==modelPet).first()
        modelName=sql_list.mode_name
        typeName=sql_list.type_name
        remote_path=sql_list.remote_path
        git_url=sql_list.git_url
        cntl_q.put({'event':'data'})
        data_q.put({'workOrder':workOrder,'typename':typeName,'modelname':modelName,'versionnumber':versionNumber,'remote_path':remote_path,'git_url':git_url[7:]})
        return web.seeother("/view/%s"%workOrder,True)

class View:

    def GET(self,workOrder):
        logList=web.ctx.orm.query(models.TaskLogs).filter(models.TaskLogs.id==workOrder).first()
        return render.view(logList=logList)

if __name__ == '__main__':
    p=mp.Process(target=pack.main,args=(cntl_q,data_q))
    p.start()
    app.run()
