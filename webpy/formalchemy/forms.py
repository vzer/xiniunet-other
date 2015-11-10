#-*- coding:utf-8 -*-
from formalchemy import config, validators, Field, FieldSet
from customEngine import Jinja2Engine
from models import *
 
class UserForm:
    def __init__(self):
        #这里的directories是指表单模板存放的地方，我们在第二章提到的templates下创建一个文件夹，命名为form
        config.engine = Jinja2Engine(directories=["templates/form"])
 
    #为表单设置label
    def setLabel(self):
        self.name = self.fs.name.label("User Name")
        self.email = self.fs.email.label("Email Address")
        self.password = self.fs.password.label("Password")
        self.superuser = self.fs.superuser.label("Admin?")

    #定义编辑模式下通用的设置，编辑模式包括：新增，修改
    def wmode(self, password=None):
        self.setLabel()
 
        #因为新增和修改中都需要用户重新确认密码，所以要为表单加入Confirm Password
        #如果有指定password的值，说明用户是在修改记录，那么Confirm Password也必须有值
        if not password:
            self.fs.insert_after(self.fs.password, Field("confirm_password"))
        else:
            self.fs.insert_after(self.fs.password, Field("confirm_password", value=password))
        self.confirm_password = self.fs.confirm_password.label("Re-enter Password")
 
        self.name = self.name.required()
        self.email = self.email.required().email().validate(validators.email)
        self.password = self.password.required().password()
        self.confirm_password = self.confirm_password.required().password()
 
    #定义新增用户时调用的方法
    def write_render(self, cls):
        #设置Fieldset对象，指定要绑定的sqlalchemy中的表类，并赋予sqlalchemy的session
        self.fs = FieldSet(User, session=cls.db)
        self.wmode()
 
        #配置表单信息
        self.fs.configure(
            #表单包含的字段
            include=[
                self.name,
                self.email,
                self.password,
                self.confirm_password,
                self.superuser
            ]
        )
        return self.fs