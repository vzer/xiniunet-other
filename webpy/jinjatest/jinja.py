#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import web
from  web.contrib.template import render_jinja


urls=(
    '/jinja','Jinja'
)

kks={'id':1,'name':'kks','email':'xxx@xiniunet.com'}
app=web.application(urls,locals())
session=web.session.Session(app,web.session.DiskStore('session'))

render_jinja=render_jinja('templates',encoding='utf-8')


class Jinja:
    def GET(self):
        return render_jinja.jinja(kks=kks)

if __name__=="__main__":
    app.run()