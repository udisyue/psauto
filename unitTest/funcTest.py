#!/usr/bin/env python
# -*- coding: utf-8 -*-
import read_conf
import sugTest
import json
import difflib
import sug_types_pb2
import sug_service_pb2
import assert_func
#print redisOp.get_multiActi(157, 43, 633344, 190000032101382281)
#print redisOp.get_joinnum(157, 43)
#redisOp.del_multiActi_value(157, 43, 633344, 190000032101382281)
#print redisOp.set_multiActi_value_0(157, 43, 633344, 190000032101382281)
#param = read_conf.read_sug('sug001.conf')
#print param
response = sugTest.sug_get('./sug_case/chn04.conf')
#print response
#print response.split('\n')
#jresp = json.dumps(response.split('\n'))
#print jresp

print response.__unicode__().encode("utf8")
