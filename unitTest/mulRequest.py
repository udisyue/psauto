#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("./")
from google.protobuf import text_format
import logging
import struct
import socket
import random
import time
import datetime
import traceback
import json
from pbTojson.pbjson import pb2json, pb2dict

from gen import price_types_pb2
from gen import as_types_pb2
from gen import price_service_pb2
import build_msg
import log_write
import handle_response
import readDict
if_coupon_on = 1

def handle_response(serialized_msg, show_type):
    response = price_service_pb2.PsResponse()
    response.ParseFromString(serialized_msg)
    # text_format.PrintMessage(response, sys.stdout)
    # return response
    # response_str = text_format.MessageToString(response)
    # return pb2json(response)
    if show_type == "1":
        # return pb2json(response)
        return json.dumps(json.loads(pb2json(response)), indent=4, sort_keys=False, ensure_ascii=False)
    else:
        return pb2dict(response)
# in_param must be json!
def list(in_param):
    in_param_dict = {}
    try:
        if type(in_param) == str:
            in_param_dict = json.loads(in_param)
        else:
            in_param_dict = in_param
    except Exception as e:
        return None

    HOST = in_param_dict["ip"]
    PORT = 0 if in_param_dict["port"] == '' else int(in_param_dict["port"])

    nshead = struct.Struct("HHI16sIII");
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = None

    try:
        # connect
        s.connect((HOST, PORT))
        # send
        msg, length = build_msg.request_list(nshead, in_param_dict, if_coupon_on)
        head = nshead.pack(1, 1, 1, "elong", 1, 0, length)
        s.sendall(head)
        s.sendall(msg)
        # receive
        data = s.recv(nshead.size)
        if len(data) == nshead.size:
            head_id, version, log_id, provider, magic, method_id, body_len = \
                nshead.unpack(data)
            if body_len != 0:
                serialized_msg = ""
                len_left = body_len
                while len_left > 0:
                    buf_size = len_left if len_left < 1024 else 1024
                    serialized_msg += s.recv(buf_size)
                    len_left -= buf_size;

                response = handle_response.response(serialized_msg, in_param_dict["show_type"])
            else:
                logging.warning("Received an empty message")
        else:
            logging.warning("Receive bad nshead header, length=%d", len(data))

        s.close()
    except socket.error, e:
        logging.warning(e)
        traceback.print_exc()
    finally:
        s.close()
    return response

def detail(in_param):
    in_param_dict = {}
    try:
        if type(in_param) == str:
            in_param_dict = json.loads(in_param)
        else:
            in_param_dict = in_param
    except Exception as e:
        return None

    HOST = in_param_dict["ip"]
    PORT = 0 if in_param_dict["port"] == '' else int(in_param_dict["port"])

    nshead = struct.Struct("HHI16sIII");
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = None

    try:
        # connect
        s.connect((HOST, PORT))
        # send
        msg, length = build_msg.request_detail(nshead, in_param_dict)
        head = nshead.pack(1, 1, 1, "elong", 1, 0, length)
        s.sendall(head)
        s.sendall(msg)
        # receive
        data = s.recv(nshead.size)
        #print len(data)
        #print nshead.size
        if len(data) == nshead.size:
            head_id, version, log_id, provider, magic, method_id, body_len = \
                nshead.unpack(data)
            if body_len != 0:
                serialized_msg = ""
                len_left = body_len
                while len_left > 0:
                    buf_size = len_left if len_left < 1024 else 1024
                    serialized_msg += s.recv(buf_size)
                    len_left -= buf_size;
                #sarray = serialized_msg.split('\n')
                #print len(sarray)
                #print sarray
                #for line in range(0,len(sarray)) :
                #    print line
                 #   print sarray[line]
                response = handle_response(serialized_msg, in_param_dict["show_type"])
            else:
                logging.warning("Received an empty message")
        else:
            logging.warning("Receive bad nshead header, length=%d", len(data))

        s.close()
    except socket.error, e:
        logging.warning(e)
        traceback.print_exc()
    finally:
        s.close()
    return response
# set param
in_param = {}
# in_param["ip"] = "192.168.14.170"
in_param["ip"] = "192.168.232.40"
in_param["port"] = "6300"
in_param["booking_channel"] = "2"
in_param["order_from"] = "50"
in_param["customer_level"] = "1"
# in_param["user_ip"] = "127.0.0.1"
in_param["hotel_id"] = "633344"
in_param["filter_ota"] = "32768"
in_param["checkin"] = "2017-04-30"
in_param["checkout"] = "2017-05-01"
in_param["adult_num"] = "2"
in_param["children"] = ""
in_param["search_id"] = "123456789"
in_param["list_query_flag"] = "7"
in_param["show_type"] = "1"
# in_param["activity_id"] = "2015081441,2015081442"
in_param["activity_id"] = ""
# print "origin: ", type(in_param)
in_param_json = json.dumps(in_param)
# print "dict 2 json: ", type(in_param_json)
in_param_dict = json.loads(in_param_json)
rlt = detail(in_param_json)
#print rlt
jrlt = json.loads(rlt)
#print jrlt['service_status']
#b_s_price = jrlt['list_response']['list_hotel'][0]['list_ota_list'][0]['base_sale_price']['average_price']['amount']
#ori_price = rlt['list_response']['list_hotel'][0]['list_ota_list'][0]['origin_price']['average_price']['amount']
#ota = rlt['list_response']['list_hotel'][0]['list_ota_list'][0]['ota_id']
#print b_s_price
#print ori_price
#print ota
#info = readDict.readAPInfo('51')
#print info
#h_lose = [info['lose_info']['lose_copy_price']['H'], info['lose_info']['lose_modify_price']['H']]
#print h_los
print jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['origin_price']['total_price']['amount']
