#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
import time
log_path = "./log/"
def mk_logfile(buff) :
    stamp = time.strftime("%Y%m%d%H%M%S",time.localtime())
    fname = log_path + stamp + '.rlt'
    fo = open(fname,'w')
    if buff :
        fo.write(buff)
    fo.close()
    return fname

def log_list_format(jdata) :
    log_list = {}
    print jdata['list_response']['list_hotel'][0]['list_ota_list'][0]['pay_type']
    if jdata['service_status']['msg'] == 'success' :
        log_list['status'] = jdata['service_status']['msg']
    #if jdata['list_response']['list_hotel']['promotion_info']  :
        #log_list['promotion']= jdata['list_response']['list_hotel']['promotion_info']
        return log_list

def log_error(buff) :
    print buff
    stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    fname = log_path + stamp + '.rlt'
    fo = open(fname, 'wb')
    fo.write(buff)
    fo.close()

def log_add(name, buff) :
    fo = open(name, 'a')
    if buff :
        fo.write(buff+'\n')
    fo.close()