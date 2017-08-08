#!/usr/bin/env python
# -*- coding: utf-8 -*-
import read_conf
import sugTest
import json
import sug_types_pb2
import sug_service_pb2
import os
import sys
import re
import assert_func
import log_write
path = "./sug_case"
files =  os.listdir(path)
cflist = []
for cnt in range(0,len(files)) :
    if re.search('conf',files[cnt]) :
        cflist.append(files[cnt])
print cflist
checklist=[]
for cnt in range(0,len(cflist)):
    response = sugTest.sug_get(path+'/'+cflist[cnt])
    #each_len是sug_response的结果个数
    each_len = len(response.sug_response)
    print path+'/'+cflist[cnt]
    checklist = read_conf.read_sug(path+'/'+cflist[cnt])
    #逐个检查sug结果中的字段
    for sugr_cnt in range(0,each_len):
        #checkpoint 1: keywords
        chk1 = assert_func.ifcontent_in(checklist[4], response.sug_response[sugr_cnt].name_cn.encode("utf8"))
        if chk1 == 1 :
            chk1_rlt = 'check point 1 : keywords %s success'%checklist[2]
        else :
            chk1_rlt = 'check point 1 : keywords %s failed'%checklist[2]
            print response.sug_response[sugr_cnt].region_info.dest_name_cn.encode("utf8")
        #checkpoint 2: sug type
        chk2_rlt_pass = []
        chk2_rlt_fail = []
        for requeire_cnt in range(0, len(checklist[3])):
            for sug_cnt in range(0,each_len):
                chk2 = assert_func.check_sugtype(checklist[3][requeire_cnt], response.sug_response[sug_cnt].type)
                if chk2 == 1 :
                    chk2_rlt_pass.append(checklist[3][requeire_cnt])
                    break
                else:
                    chk2_rlt_fail.append(checklist[3][requeire_cnt])
        chk2_rlt = 'check point 2 : sug type %r pass, sug type %r fail'%(chk2_rlt_pass, chk2_rlt_fail)
        print chk1_rlt
        print chk2_rlt
