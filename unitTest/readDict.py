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
            info = 0
    jinfo = json.loads(info[1])
    return jinfo