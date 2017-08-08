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

def main():
    hot_dest = read_conf.read_hotRegion()
    for i in range(0,len(hot_dest)):
        dest_cn_name = read_conf.region_match(hot_dest[i])
        response = sugTest.sug_hotRegion(dest_cn_name)
        for j in range(0,len(response.sug_response)):
            print response.sug_response[j].name_cn.encode("utf8")
if __name__ == "__main__":
    print main()
