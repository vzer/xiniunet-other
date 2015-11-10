#!/usr/bin/env python
#-*- coding:utf-8 -*-
from formalchemy import templates
from jinja2 import Environment,FileSystemLoader

#定义一个方法用来获取formalchemy输出input的name属性
def field_label(field):
    return field.parent._format % dict([('model',field.model.__class__.__name__), ('pk',field.parent.model.id or ''), ('name',field.name)])

#定义一个方法用来获取formalchemy中定义字段的label
def field_name(field):
    return field.label_text or field.name

class Jinja2Engine(templates.TemplateEngine):
    extension = 'jinja2'
    def get_template(self, name, **kw):
        self._lookup = Environment(loader=FileSystemLoader(self.directories, **kw))
        self._lookup.filters.update(
            #如果你想要在模板里添加filter，可以在这里添加
            field_label = field_label,
            field_name = field_name,
        )
        #增加这个扩展可以让我们在模板的循环块里使用break，continue
        self._lookup.add_extension('jinja2.ext.loopcontrols')
        #增加这个扩展可以让我们在模板里使用do关键字，用来进行一些python语句操作
        self._lookup.add_extension('jinja2.ext.do')
        return self._lookup.get_template("%s.%s" % (name, self.extension))

    def render(self, template_name, **kwargs):
        template = self._lookup.get_template("%s.%s" % (template_name, self.extension))
        return template.render(**kwargs)