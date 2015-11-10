#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

import web
web.config.debug=True


urls=(
    '/count','Count',
    '/reset','Reset'
)


app=web.application(urls,locals())
if web.config.get('_session') is None:
    print 'A'
    session=web.session.Session(app,web.session.DiskStore('sessionss'),initializer={'count':0})
    web.config._session=session
else:
    print "B"
    session=web.config._session

class Count:
    def GET(self):
        print session
        session.count=session.count+1
        return str(session.count)


class Reset:
    def GET(self):
        session.kill()
        return ''

if __name__=="__main__":
    app.run()