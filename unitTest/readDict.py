#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import json
def readAPRule(start, tstamp):
    fo = open('auto_price_rule.dict','r')
    ruleBuf = fo.readlines()
    for cnt in range(start,len(ruleBuf)) :
        content = re.sub(r'\n', "", ruleBuf[cnt])
        tmprule = content.split('\t')
        print tmprule
        if tmprule[2] == tstamp :
            print tmprule
            fo.close()
            offset = cnt + 1
            rule = tmprule
            break
        else :
            fo.close()
            offset = 0
            rule = 0
    return offset,rule

def readAPInfo(id):
    fo = open('auto_price_info.dict','r')
    infoBuf = fo.readlines()
    for cnt in range(0,len(infoBuf)):
        content = re.sub(r'\n',"", infoBuf[cnt])
        tmpinfo = content.split('\t')
        if tmpinfo[0] == id :
            fo.close()
            info = tmpinfo
            break
        else :
            fo.close()
            info = 0
    jinfo = json.loads(info[1])
    return jinfo

def readManualDis(id):
    fo = open('manual_price_tool.dict', 'r')
    infoBuf = fo.readlines()
    for cnt in range(0,len(infoBuf)):
        content = re.sub(r'\n',"", infoBuf[cnt])
        tmpinfo = content.split('\t')
        if tmpinfo[0] == id:
            fo.close()
            info = tmpinfo
            break
        else :
            info = 0
    if info == 0 :
        for cnt in range(0, len(infoBuf)):
            content = re.sub(r'\n', "", infoBuf[cnt])
            tmpinfo = content.split('\t')
            if tmpinfo[0] == '*' and tmpinfo[1] == '*':
                fo.close()
                info = tmpinfo
                break
            else :
                info = 0
    print info[5]
    jinfo = json.loads(info[5])
    return jinfo

def idChcek(id, tstamp, channel):
    fo = open('auto_price_rule.dict', 'r')
    ruleBuf = fo.readlines()
    print ruleBuf
    for cnt in range(0, len(ruleBuf)):
        content = re.sub(r'\n', "", ruleBuf[cnt])
        tmprule = content.split('\t')
        print cnt
        if tmprule[0] == id and tmprule[1] == channel and tmprule[2] == tstamp:
            fo.close()
            flag = 1
            break
        else :
            fo.close()
            flag = 0
    if flag == 1:
        fo2 = open('rule_blacklist.dict', 'r')
        blacklist = fo2.readlines()
        for cnt2 in range(0, len(blacklist)):
            content = re.sub(r'\n', "", blacklist[cnt2])
            tmprule = content.split('\t')
            if tmprule[0] == id and tmprule[2] == 1:
                flag = 1
            else :
                flag = 0

    return flag


