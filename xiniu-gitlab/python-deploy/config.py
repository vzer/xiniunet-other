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
    {"foundation":("10.168.246.1","10.168.245.116",),},
    {"backend":("10.168.246.33","10.168.245.136",),},
    {"marketplace":("10.161.222.50","10.162.69.8",),},
    {"financial":("10.168.242.11","10.168.245.63",),},
    {"distribution":("10.168.246.156","10.168.240.230",),},
    {"platform":("10.168.245.72",),},
    {"site":("10.117.210.244",),},
    {"integration":("10.168.79.58",),},
    {"collaboration":("10.51.19.158",),},
    {"relationship":("10.169.2.205",),},
    {"logistics":("10.168.239.141","10.117.40.77",),},
    {"globalwinner-app":("10.168.10.224",),},
    {"dfl-backend":("10.252.164.150",),},
)

#前台web主机ip地址集合
#前台web地址信息
prowebLocalPath="/xiniu/updatewar/"
prowebScriptFile="releasewebdeploy.sh"
ProduceWebIp=(
    {"siteweb":("10.165.99.21",),},
    {"www":("10.168.246.170","10.168.246.18",),},
    {"auth":("10.168.247.181","10.168.247.32",),},
    {"employee":("10.168.241.196","10.168.241.37",),},
    {"service":("10.168.245.46","10.168.247.8",),},
    {"open":("10.161.222.50","10.162.69.8",),},
    {"member":("10.168.228.222","10.168.244.216",),},
    {"my":("10.169.2.233","10.251.237.129",),},
    {"product1":("10.168.244.177",),},
    {"web-backend":("10.168.245.33","10.168.240.171",),},
    {"web-financial":("10.168.242.77","10.168.247.211",),},
    {"web-distribution":("10.168.26.126","10.171.224.10",),},
    {"web-marketplace":("10.168.36.98","10.171.198.100",),},
    {"web-collaboration":("10.168.244.155",),},
    {"web-logistics":("No host",),},
    {"harson-supplychain":("10.51.26.87","10.117.26.29",),},
    {"harson-distribution":("10.51.1.131","10.117.29.219",),},
    {"harson-ecommerce":("10.51.26.168","10.117.106.201",),},
    {"web-relationship":("10.171.211.26",),},
    {"web-integration":("10.171.252.132",),},
    {"dfl":("10.168.252.251",),},
    {"dfl-api":("10.51.25.204",),},
    {"web-dfl-backend":("10.161.187.147",),},
)

#job类主机ip地址
#job类工程地址信息
projobLocalPath="/xiniu/updateapps/"
projobScriptFile="queuedeploy.sh"
ProduceJobIp=(
    {"globalwinner-job":("10.168.127.205","121.40.241.67"),},
)
#++++++++++++++++++++++++++++++++++++++++生产老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#

#++++++++++++++++++++++++++++++++++++++++生产platform平台环境++++++++++++++++++++++++++++++++++++++++++++++++++#
#后台服务主机ip地址集合
proplatserviceLocalPath="/xiniu/platform-updateapps/"
proplatserviceScriptFile="releaseservicedeploy.sh"
ProducePlatformServiceIp=(
    {"communication":("10.132.5.246","10.168.112.65",),},
    {"data":("10.168.174.8","10.162.59.145",),},
    {"distribution":("10.161.181.91","10.162.66.237",),},
    {"framework":("No host","No host",),},
    {"foundation":("10.160.80.235","10.251.248.103",),},
    {"financial":("10.161.226.73","10.161.217.1",),},
    {"integration":("10.162.69.85","10.169.7.132",),},
    {"log":("10.168.242.252","10.160.62.85",),},
    {"membership":("10.162.87.197","10.252.93.30",),},
    {"master":("10.161.217.4","10.252.86.10",),},
    {"promotion":("10.168.59.133","10.171.252.53",),},
    {"retail":("10.160.14.241","10.162.61.234",),},
    {"security":("10.161.189.104","10.168.127.8",),},
    {"sdk":("No host","No host",),},

)

#前台web主机ip地址集合
#前台web地址信息
proplatwebLocalPath="/xiniu/platform-updatewar/"
proplatwebScriptFile="releasewebdeploy.sh"
ProducePlatformWebIp=(
    {"api":("10.160.39.64","10.117.16.169",),},
    {"pos-web":("10.160.12.221","10.168.2.48",),},
    {"pos-api":("10.252.251.123","10.174.176.73",),},
    {"pos-ult":("10.132.74.94","10.161.218.206",),},
)

#job类主机ip地址
#job类工程地址信息
proplatjobLocalPath="/xiniu/updateapps/"
proplatjobScriptFile="queuedeploy.sh"
ProducePlatformJobIp=(
    {"":("","",),},
)
#++++++++++++++++++++++++++++++++++++++++生产platform平台环境++++++++++++++++++++++++++++++++++++++++++++++++++#
########################################生产环境变量配置############################################################

########################################预发布环境变量配置############################################################
#++++++++++++++++++++++++++++++++++++++++ 预发布老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#
#后台服务主机ip地址集合
#后台服务地址信息
preserviceLocalPath="/xiniu/updateapps/"
preserviceScriptFile="releasepreservicedeploy.sh"
PreServiceIp=(
    {"foundation":("10.175.195.205",),},
    {"backend":("10.175.193.173",),},
    {"marketplace":("10.168.43.167",),},
    {"financial":("10.175.199.178",),},
    {"distribution":("10.168.43.181",),},
    {"platform":("10.117.34.172",),},
    {"site":("No host",),},
    {"integration":("10.171.208.220",),},
    {"collaboration":("No host",),},
    {"relationship":("No host",),},
    {"logistics":("10.171.237.84",),},
)

#前台web主机ip地址集合
#前台web地址信息
prewebLocalPath="/xiniu/updatewar/"
prewebScriptFile="releaseprewebdeploy.sh"
PreWebIp=(
    {"siteweb":("",),},
    {"www":("10.168.30.86",),},
    {"auth":("10.175.197.178",),},
    {"employee":("10.165.98.2",),},
    {"service":("10.171.211.111",),},
    {"open":("10.252.147.252",),},
    {"member":("10.175.196.122",),},
    {"my":("10.175.197.5",),},
    {"product1":("10.171.242.51",),},
    {"web-backend":("10.175.197.13",),},
    {"web-financial":("10.171.220.251",),},
    {"web-distribution":("10.171.208.136",),},
    {"web-marketplace":("10.171.245.222",),},
    {"web-collaboration":("No host",),},
    {"web-logistics":("No host",),},
    {"harson-supplychain":("10.51.23.145",),},
    {"harson-distribution":("10.117.48.133",),},
    {"harson-ecommerce":("10.117.109.57",),},
    {"web-relationship":("No host",),},
    {"web-integration":("10.252.85.217",),},
    {"dfl":("No host",),},
)
#job类主机ip地址
#job类工程地址信息
prejobLocalPath="/xiniu/updateapps/"
prejobScriptFile="queuedeploy.sh"
PreJobIp=(
    {"globalwinner-job":("No host",),},
)
#++++++++++++++++++++++++++++++++++++++++预发布老整合环境++++++++++++++++++++++++++++++++++++++++++++++++++#

#++++++++++++++++++++++++++++++++++++++++预发布platform平台环境++++++++++++++++++++++++++++++++++++++++++++++++++#
#后台服务主机ip地址集合
preplatserviceLocalPath="/xiniu/platform-updateapps/"
preplatserviceScriptFile="releasepreservicedeploy.sh"
PrePlatformServiceIp=(
    {"communication":("10.117.38.53",),},
    {"data":("10.117.178.206",),},
    {"distribution":("10.252.86.51",),},
    {"framework":("No host",),},
    {"foundation":("10.160.5.46",),},
    {"financial":("10.251.236.25",),},
    {"integration":("10.132.61.28",),},
    {"log":("10.160.16.213",),},
    {"membership":("10.161.217.18",),},
    {"master":("10.51.25.179",),},
    {"promotion":("10.161.210.168",),},
    {"retail":("10.161.217.139",),},
    {"security":("10.168.163.113",),},
    {"sdk":("No host",),},

)

#前台web主机ip地址集合
#前台web地址信息
preplatwebLocalPath="/xiniu/platform-updatewar/"
preplatwebScriptFile="releaseprewebdeploy.sh"
PrePlatformWebIp=(
    {"api":("10.161.173.208",),},
    {"pos-web":("10.171.216.149",),},
    {"pos-api":("10.117.11.202",),},
    {"pos-ult":("10.160.27.8",),},
)

#job类主机ip地址
#job类工程地址信息
preplatjobLocalPath="/xiniu/updateapps/"
preplatjobScriptFile="queuedeploy.sh"
PrePlatformJobIp=(
    {"":("","",),},
)
#++++++++++++++++++++++++++++++++++++++++预发布platform平台环境++++++++++++++++++++++++++++++++++++++++++++++++++#

########################################预发布环境变量配置############################################################




#账户信息
user="root"
password="xiniunet_#2105"

