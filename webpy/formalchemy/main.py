#!/usr/bin/env python
#-*- coding:utf-8 -*-
import web, middleware
from web.contrib.template import render_jinja
from models import *
from forms import *
 
urls = (
    "/", "index",
    "/form/", "showform",
)
app = web.application(urls, globals())
app.add_processor(middleware.set_orm)
 
render = render_jinja(
    'templates',
    encoding = 'utf-8',
)
 
class BaseView(object):
    def __init__(self):
        #从web.ctx.orm获取session放入基类的db中
        self.db = web.ctx.orm
 
class index(BaseView):
    def GET(self):
        return render.index()
 
class showform(BaseView):
    def GET(self):
        form = UserForm()
        fs = form.write_render(self)
        return render.form(form=fs)
 
if __name__ == "__main__":
    app.run()