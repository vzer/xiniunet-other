#!/usr/bin/env python
# -*- coding: utf-8 -*-
#filename:portal.py
__author__ = 'vzer'

import web
import datetime
import os
from web import form
from web.session import Session
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
web.config.debug=False

class MySessionExpired(web.HTTPError):
    def __init__(self, headers,message):
        web.HTTPError.__init__(self, '200 OK', headers, data=message)

class MySession(Session):
    def __init__(self, app, store, initializer=None):
        Session.__init__(self,app,store,initializer)

    def expired(self):
        self._killed = True
        self._save()
        message = self._config.expired_message
        headers = {
            "http-equiv":"refresh",
            "content":"3;url=/login",
        }
        raise MySessionExpired(headers, message)

urls=(  '/','Login',
        '/login','Login',
        '/reg','Reg',
        '/logout','Logout',
        '/showusers','Showusers',
        '/changepd','Changepd',
        '/lookwin7','Lookwin7',
        '/lookwin8','Lookwin8',
        '/lookiphone','Lookiphone',
        '/notfound','NotFound404'
      )

db=web.database(dbn='mysql',
                user='vzer',
                pw='vzer',
                host='192.168.1.245',
                port=3306,
                db='radius',
                charset='utf8')
app=web.application(urls,globals())
render=web.template.render("templates")
session=web.session.Session(app,web.session.DiskStore('sessions'),initializer={'Login':0,'username':''})
#session=MySession(app,web.session.DiskStore('sessions'),initializer={'Login':0,'username':''})

###win7教程页面
class Lookwin7:
    def GET(self):
        return render.lookwin7(u"windows XP & 7连接教程")

    def POST(self):
        return ''

###win8教程页面
class Lookwin8:
    def GET(self):
        return render.lookwin8(u"windows 8连接教程")

    def POST(self):
        return ''

###win8教程页面
class Lookiphone:
    def GET(self):
        return render.lookiphone(u"Iphone&Android连接教程")

    def POST(self):
        return ''

###登陆页面
class Login:
    def GET(self):
        if logged():
             raise web.seeother('/showusers')
        else:
            return render.login(u"")
        #return render.login(self.loginForm)
    def POST(self):
        postdata=web.input()
        username=web.net.websafe(postdata.username)
        password=web.net.websafe(postdata.password)
        rslist=getUserByUserName(username)
        if len(rslist)==0:
            return render.login(u'用户名不存在')
        else:
            if password==rslist[0].value:
                session.Login=1
                session.username=username
                #return render.login(self.loginForm,u'登陆成功,欢迎你:'+username)
                raise web.seeother('/showusers')
            else:
                return render.login(u'用户名及密码不匹配')


###注册页
class Reg:
    def GET(self):
        return render.reg(u"")

    def POST(self):
        formdata=web.input()
        username=web.net.websafe(formdata.username)
        password=web.net.websafe(formdata.password)
        password2=web.net.websafe(formdata.passwordsignup_confirm)
        company=web.net.websafe(formdata.company)
        regip=web.ctx.ip
        regdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if password!=password2:
            return render.reg(u"两次密码不一致")
        #判断用户名是否存在:
        else:
                if len(getUserByUserName(username))>0:
                    return render.reg(u'用户名已存在')
                else:
                    ret=addUser(username,password,regdate,regip,company)
                    ret1=linkGroup(username)
                    if ret!=0:
                        session.Login=1
                        session.username=username
                        raise web.seeother('/showusers')
                    else:
                        return render.reg(u'注册失败')


###修改密码
class Changepd:
    def GET(self):
        return render.changepd(u"")

    def POST(self):
        formdata=web.input()
        passwordold=web.net.websafe(formdata.passwordold)
        passwordnew=web.net.websafe(formdata.passwordnew)
        passwordnew2=web.net.websafe(formdata.passwordnewsignup_confirm)
        changeip=web.ctx.ip
        if passwordnew!=passwordnew2:
            return render.reg(u"两次密码不一致")
        ret=changepw(session.username,passwordnew,changeip)
        if ret!=0:
            raise web.seeother('/showusers/'+session.username)
        else:
            return render.reg(u'注册失败')


###注销登陆页面
class Logout:
    def GET(self):
        session.Login=0
        session.username=''
        session.kill()
        return render.logout(u'注销成功,欢迎下次登录....')

###404not found页面
class NotFound404:
    def GET(self):
        return render.notfound()



###显示用户列表
class Showusers:
    def GET(self):
        if logged():
            usersList=getUsers(username=session.username)
            return render.users(usersList)
            #return usersList
        else:
            return u'对不起 您没有登陆无权查看'

###判断用户是否登陆
def logged():
    if session.Login==1:
        return True
    else:
        return False


def notfound():
    return web.notfound(render.notfound())


################################################ 数据库操作部分 begin ############################################################

#增加用户
def addUser(username,password,regdate,regip,company):
    ret=db.insert('radcheck',username=username ,attribute='Cleartext-Password',op=':=',value=password,createtime=regdate,regip=regip,company=company)
    return ret

#修改密码
def changepw(username,password,changeip):
    ret=db.update('radcheck',where='username=$username',value=password,regip=changeip,vars=locals())
    return ret
#关联群组
def linkGroup(username):
    ret=db.insert('radusergroup',username=username,groupname='user')
    return set

#获取用户列表
def getUsers(username):
    rs=db.select('radcheck',where='username="'+username+'"')
    rslist=[]
    for r in rs:
        rslist.append(r)
    return rslist

#根据用户名查询用户信息
def getUserByUserName(username):
    rs=db.select('radcheck',where='username="'+username+'"')
    rslist=[]
    for r in rs:
        rslist.append(r)
    return rslist

################################################ 数据库操作部分 end ########################################
app.notfound = notfound
if __name__=="__main__":
    app.run()