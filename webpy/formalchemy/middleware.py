#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import *
import web
 
def set_orm(handler):
    #获取sqlalchemy的session并存储到web.ctx.orm中
    web.ctx.orm = bindSQL()
    #执行视图，如果出现异常回滚数据库，正常结束则提交数据库操作，最终删除session
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.rollback()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        web.ctx.orm.remove()