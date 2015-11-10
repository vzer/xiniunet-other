# -*- coding:utf-8 -*-
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib
 
#这里定义一个password加密混淆
password_prefix = "Ad%cvcsadefr^!deaf"
 
#定义数据库的账号、端口、密码、数据库名，使用的连接模块，这里用的是mysqldb
engine = create_engine(
    'mysql+mysqldb://vzer:wwwlin123@192.168.1.246:3306/hosts?charset=utf8',
    echo=False#是否输出数据库操作过程，很方便调试
)
 
#定义一个函数，用来获取sqlalchemy的session
def bindSQL():
    return scoped_session(sessionmaker(bind=engine))
 
Base = declarative_base()
Base.__table_args__ = {'mysql_engine':'InnoDB'}#定义数据表使用InnoDB
 
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    email = Column(String(32), unique=True)
    password = Column(String(32))
    superuser = Column(Boolean, default=False)
 
metadata = Base.metadata
 
#定义一个回调函数用于响应触发事件
def setPassword(target, value, oldvalue, initiator):
    if value == oldvalue:#如果新设置的值与原有的值相等，那么说明用户并没有修改密码，返回原先的值
        return oldvalue
    #如果新值与旧值不同，说明密码发生改变，进行加密，加密方法可以根据自己需求改变
    return hashlib.md5("%s%s" % (password_prefix, value)).hexdigest()
#设置事件监听，event.listen(表单或表单字段, 触发事件, 回调函数, 是否改变插入值)
event.listen(User.password, "set", setPassword, retval=True)
 
#为了避免重复插入数据，定义一个get_or_create函数，这个是模仿django的，有兴趣的同学可以google下
def get_or_create(session, model, **kwargs):
    if "defaults" in kwargs:
        defaults = kwargs["defaults"]
        del kwargs["defaults"]
    else:
        defaults = {}
 
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        kwargs.update(defaults)
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        session.refresh(instance)
        return instance, True
 
#定义初始化函数
def initModel():
    metadata.create_all(engine)#创建数据库
    db = bindSQL()#获取sqlalchemy的session
    #创建超级管理员，这里为了避免多次运行initModel而发生重复插入的情况，使用了get_or_create方法
    obj, created = get_or_create(
        db,
        User,
        name="administrator",
        defaults={
            "email": "332535694@qq.com",
            "password": "administrator",
            "superuser": True
        }
    )
    db.commit()#记得commit喔，不然数据最后还是没插入
    db.remove()
 
if __name__ == "__main__":
    initModel()