#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from xml.etree import ElementTree as ET

tree=ET.parse("D:/pom.xml")
root=tree.getroot()
for key in root:
    if key.tag=="{http://maven.apache.org/POM/4.0.0}version":
        if "SNAPSHOT" in key.text.upper() or "RELEASE" in key.text.upper():
            print 1
