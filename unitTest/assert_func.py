#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
def ifcontent_in(content, result_buf):
    check_point = re.search(content, result_buf)
    if check_point :
        return 1
    else:
        return 0

def ifcontent_out(content, result_buf):
    check_point = re.search(content, result_buf)
    if check_point:
        return 0
    else:
        return 1

def content_diff(content_a,content_b):
#检查入参类型,int,float,str,set,list
    typeA = ''
    typeB = ''
    if content_a and content_b :
        if isinstance(content_a, int):
            typeA = 'int'
        elif isinstance(content_a, str):
            typeA = 'str'
        elif isinstance(content_a, float):
            typeA = 'float'
        elif isinstance(content_a, list):
            typeA = 'list'
        elif isinstance(content_a, set):
            typeA = 'set'
        else :
            typeA = 'tuple'
        print typeA
        if isinstance(content_b, int):
            typeB = 'int'
        elif isinstance(content_b, str):
            typeB = 'str'
        elif isinstance(content_b, float):
            typeB = 'float'
        elif isinstance(content_b, list):
            typeB = 'list'
        elif isinstance(content_b, set):
            typeB = 'set'
        else:
            typeB = 'tuple'
        print typeB
        if typeA == typeB :
            if content_a == content_b :
                return 1
            else:
                return 0
        else:
            return 0
    else :
        return 0

def check_sugtype(typecode, type) :
    '''if typecode == 0:
        sugtype = 'UNKNOW'
    elif typecode == 1:
        sugtype ='IHOTEL_CITY' #城市
    elif typecode == 2:
        sugtype = 'IHOTEL_POI' #poi
    elif typecode == 3:
        sugtype = 'IHOTEL_NEIGHBOR' #商圈
    elif typecode == 4:
        sugtype = 'IHOTEL_COUNTRY'  #国家
    elif typecode == 5:
        sugtype = 'IHOTEL_TOPIC'  #主题
    elif typecode == 6:
        sugtype = 'IHOTEL_HOTEL'  #酒店
        '''
    #check = re.search(sugtype, type)
    if typecode == type :
        return 1
    else:
        return 0
