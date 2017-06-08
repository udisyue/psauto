#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.protobuf import text_format
import sys
import os

sys.path.append("./gen")
import logging
import struct
import socket
import random
import time
import datetime
import traceback
import read_conf
import sug_service_pb2
import sug_types_pb2
HOST = '192.168.232.14'
#HOST = '192.168.94.60'
PORT = 5210
'''
pbcmd1 = "/home/yuzhong.chen/git/base/third-64/protobuf/bin/protoc --python_out=. --proto_path=../interface/ ../interface/sug_types.proto"
pbcmd2 = "/home/yuzhong.chen/git/base/third-64/protobuf/bin/protoc --python_out=. --proto_path=../interface/ ../interface/sug_service.proto"

if not os.path.exists(r'./sug_types_pb2.py'):
    os.system(pbcmd1)
if not os.path.exists(r'./sug_service_pb2.py'):
    os.system(pbcmd2)
if os.path.exists(r'./sug_types_pb2.py') and os.path.exists(r'./sug_service_pb2.py'):
    import sug_service_pb2
    import sug_types_pb2
else:
    print "pb file not found!"
    exit(1)
'''

def build_message(nshead, param):
    request = sug_service_pb2.SugRequest()
    # version_id
    request.version_id = 2
    # user_info
    request.user_info.user_ip = "192.168.21.1"
    request.user_info.session_id = "abc"
    request.user_info.cookie_id = "def"
    request.user_info.customer_level = 0
    request.user_info.order_from = 50
    #request.user_info.booking_channel = 2
    # coupon info
    # request.user_info.activity_id_list.append(1)
    # request.user_info.activity_id_list.append(2)
    # request.user_info.activity_id_list.append(4)
    # search_type
    # request.region_id = 0;
    try:
        request.user_info.booking_channel = 2 if param[0] == '' else int(param[0])
        request.require_cnt = 10 if param[1] == '' else int(param[1])
        request.keywords = '' if param[2] == '' else param[2]
        sugTypeCnt = len(param[3])
        for cnt in range(0, sugTypeCnt):
            request.require_list.append(param[3][cnt])
    except Exception as e:
        print e
        return "", 0

    #request.require_cnt = 1;
    #request.require_list.append(1);
    #request.require_list.append(2);
    #request.require_list.append(3);
    #request.require_list.append(6);
    request.service_type = 1
    # list_req - query_info
    #request.keywords = u'niuyue'
    #print request.__unicode__().encode("utf8")
    return request, request.SerializeToString(), request.ByteSize()


def handle_response(serialized_msg):
    response = sug_service_pb2.SugResponse()
    response.ParseFromString(serialized_msg)
    # text_format.PrintMessage(response, sys.stdout)
    uresponse = response.__unicode__().encode("utf8")
    #print response.sug_response[0].__unicode__().encode("utf8")
    #print response.sug_response[0].name_match
    return response

def sug_get(fname):
    nshead = struct.Struct("HHI16sIII")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request = None
    response = None
    param = read_conf.read_sug(fname)
    try:
        # connect
        s.connect((HOST, PORT))
        # send
        request, msg, length = build_message(nshead, param)
        head = nshead.pack(1, 1, 1, "elong", 1, 0, length)
        s.sendall(head)
        s.sendall(msg)
        # receive
        # time.sleep(1)
        data = s.recv(nshead.size)
        # print len(data)
        if len(data) == nshead.size:
            head_id, version, log_id, provider, magic, method_id, body_len = \
                nshead.unpack(data)

            if body_len != 0:
                serialized_msg = ""
                len_left = body_len
                while len_left > 0:
                    buf_size = len_left if len_left < 1024 else 1024
                    temp_buf = s.recv(buf_size)
                    serialized_msg += temp_buf
                    len_left -= len(temp_buf)
                response = handle_response(serialized_msg)
            else:
                print "Received an empty message"
        else:
            logging.warning("Receive bad nshead header, length=%d", len(data))

        s.close()
    except socket.error, e:
        logging.warning(e)
        traceback.print_exc()
    finally:
        s.close()
    return response
