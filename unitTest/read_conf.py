#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
import time
import re
import simplejson
import os
def rdconf(cfname):
    fo = open(cfname, 'r')
    conf = fo.readlines()
    fo.close()
    cnt = len(conf)
    print conf
    inparse = []
    for i in range(0,cnt):
        content =  re.sub(r'\n', "", conf[i])
        search_str = re.search(r'=(.*\S)', content, re.M | re.I)
        print search_str.group(1)
        if search_str.group(1)=='null':
            cfg = re.sub(r'null', "", search_str.group(1))
        else :
            cfg = search_str.group(1)
        inparse.append(cfg)
    return inparse
'''
#def get_cfname(fname):
fname = 'conf_list'
fo = open(fname, 'r')
conf_ls = fo.readlines()
list_cnt = len(conf_ls)
fo.close()
for i in range(0,list_cnt):
    enter = re.sub(r'\n', "", conf_ls[i])
    print rdconf(enter)
'''
def read_sug(cfname):
    fo = open(cfname, 'r')
    conf = fo.readlines()
    fo.close()
    cnt = len(conf)
    inparse = []
    for i in range(0, cnt):
        #读取配置中全部内容,并删除回车符
        content = re.sub(r'\n', "", conf[i])
        #读取配置中的值
        search_str = re.search(r'=(.*\S)', content, re.M | re.I)
        if search_str.group(1) == 'null':
            #将空值去掉
            cfg = re.sub(r'null', "", search_str.group(1))
        else:
            cfg = search_str.group(1)
            #第三行配置特殊处理
            if i == cnt-2:
                cfg = eval(cfg)
        #将入参放入inparse list中
        inparse.append(cfg)
    return inparse

def read_hotRegion():
    out = os.popen("cat dest_search_cnt.txt | grep -v \"50000$\" | grep -v \"300000\" | sort -k 2 -nr | head -n 1 |awk 'NR>=1{print $1}'")
    return out.read().split('\n')

def region_match(rid):
    dest = open('dest_info.txt','r')
    content = dest.readlines()
    for i in range(0,len(content)):
        if re.match(rid, content[i]):
            break
    #dest cn name is content[i].split('\t')[4]
    return content[i].split('\t')[4]
