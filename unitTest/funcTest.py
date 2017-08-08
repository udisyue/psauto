#!/usr/bin/env python
# -*- coding: utf-8 -*-
import read_conf
import sugTest
import json
import difflib
import sug_types_pb2
import sug_service_pb2
import assert_func
import log_write
import readDict
import sys
import os
import re
#print redisOp.get_multiActi(157, 43, 633344, 190000032101382281)
#print redisOp.get_joinnum(157, 43)
#redisOp.del_multiActi_value(157, 43, 633344, 190000032101382281)
#print redisOp.set_multiActi_value_0(157, 43, 633344, 190000032101382281)
#param = read_conf.read_sug('sug001.conf')
#print param
#response = sugTest.sug_get('./sug_case/noresult_2.conf')
#print response.__unicode__().encode("utf8")
#print response
#print response.split('\n')
#jresp = json.dumps(response.split('\n'))
#print jresp
'''
print response.__unicode__().encode("utf8")
name = log_write.mk_logfile("test")
for i in range(0,10) :
    print response.sug_response[i].name_cn
    print response.sug_response[i].region_info.dest_name_cn.encode("utf8")
    print response.sug_response[i].weight
    print response.sug_response[i].type
    log_write.log_add(name, response.sug_response[i].name_cn.encode("utf8"))
#print  assert_func.ifcontent_in("IHOTEL_NEIGHBOR", response.sug_response[0].region_info.dest_name_cn.encode("utf8"))
'''
'''
for i in range(0,10) :
    print response.sug_response[i].name_cn
    print response.sug_response[i].region_info.dest_name_cn.encode("utf8")
    print response.sug_response[i].weight
    print response.sug_response[i].type
'''
'''
info = readDict.readManualDis(1)
print info
flag = readDict.idChcek(220672,20170717,32)
print flag
'''
#print readDict.selfName()
def region_match(rid):
    dest = open('dest_info.txt','r')
    content = dest.readlines()
    for i in range(1,len(content)):
        if re.match(rid, content[i]):
            break
    return content[i]
print region_match('178236')
print region_match('178236').split('\t')[4]