#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
import time
import re
import simplejson
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
        content = re.sub(r'\n', "", conf[i])
        search_str = re.search(r'=(.*\S)', content, re.M | re.I)
        if search_str.group(1) == 'null':
            cfg = re.sub(r'null', "", search_str.group(1))
        else:
            cfg = search_str.group(1)
            if i == cnt-2:
                cfg = eval(cfg)
        inparse.append(cfg)
    return inparse