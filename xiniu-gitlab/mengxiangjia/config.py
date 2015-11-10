#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

########################################生产环境变量配置############################################################
#++++++++++++++++++++++++++++++++++++++++生产老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#
#后台服务主机ip地址集合
#后台服务地址信息
proserviceLocalPath="/xiniu/updateapps/"
proserviceScriptFile="releaseservicedeploy.sh"
ProduceServiceIp=(
    {"no Services":("No host",),},
)

#前台web主机ip地址集合
#前台web地址信息
prowebLocalPath="/xiniu/updatewar/"
prowebScriptFile="releasewebdeploy.sh"
ProduceWebIp=(
    {"anotherU":("10.105.34.103",),},
)

#job类主机ip地址
#job类工程地址信息
projobLocalPath="/xiniu/updateapps/"
projobScriptFile="queuedeploy.sh"
ProduceJobIp=(
    {"no Services":("No host",),},
)
#++++++++++++++++++++++++++++++++++++++++生产老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#
########################################生产环境变量配置############################################################




########################################预发布环境变量配置############################################################
#++++++++++++++++++++++++++++++++++++++++ 预发布老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#
#后台服务主机ip地址集合
#后台服务地址信息
preserviceLocalPath="/xiniu/updateapps/"
preserviceScriptFile="releasepreservicedeploy.sh"
PreServiceIp=(
    {"no Services":("No host",),},
)

#前台web主机ip地址集合
#前台web地址信息
prewebLocalPath="/xiniu/updatewar/"
prewebScriptFile="releaseprewebdeploy.sh"
PreWebIp=(
    {"no Services":("No host",),},
)
#job类主机ip地址
#job类工程地址信息
prejobLocalPath="/xiniu/updateapps/"
prejobScriptFile="queuedeploy.sh"
PreJobIp=(
    {"globalwinner-job":("No host",),},
)
#++++++++++++++++++++++++++++++++++++++++预发布老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#
########################################预发布环境变量配置############################################################




#账户信息
user="root"
password="Xiniunet2105"

