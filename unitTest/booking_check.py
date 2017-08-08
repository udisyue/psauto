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
import re
from gen import price_types_pb2
from gen import as_types_pb2
from gen import price_service_pb2
import build_msg
import log_write
import handle_response
import readDict
import mbl_math
if_coupon_on = 1


# in_param must be json!
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


def booking(in_param):
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
        msg, length = build_msg.request_booking(nshead, in_param_dict)
        head = nshead.pack(1, 1, 1, "elong", 1, 0, length)
        s.sendall(head)
        s.sendall(msg)
        # receive
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
                    serialized_msg += s.recv(buf_size)
                    len_left -= buf_size;

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

citime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
cotime = time.strftime('%Y-%m-%d',time.localtime(time.time()+86400))
cur_time = re.sub(r'-', "", citime)
while(1):
    # set param
    in_param = {}
    # in_param["ip"] = "192.168.14.170"
    in_param["ip"] = "192.168.232.40"
    in_param["port"] = "6300"
    in_param["booking_channel"] = 2
    in_param["order_from"] = "50"
    in_param["customer_level"] = "1"
    # in_param["user_ip"] = "127.0.0.1"
    in_param["hotel_id"] = "324763"
    in_param["filter_ota"] = "8"

    in_param["checkin"] = citime
    in_param["checkout"] = cotime
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
    jrlt = json.loads(rlt)
    if jrlt['service_status']['msg'] == 'success' and jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['hotel_status']==2:
        ota_sign = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['ota_sign']
        elong_pid = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['elong_pid']
        ota = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['ota_id']
        break
    else :
        citime += citime
        cotime += cotime
        continue
in_param = {}
in_param["ip"] = "192.168.232.40"
in_param["port"] = "6300"
in_param["booking_channel"] = "2"
in_param["order_from"] = "0"
in_param["customer_level"] = "0"
# in_param["user_ip"] = "127.0.0.1"
in_param["user_id"] = ""
in_param["hotel_id"] = "324763"
in_param["otaid"] = ota
in_param["src_otaid"] = "2"
in_param["filter_ota"] = "4"
in_param["checkin"] = citime
in_param["checkout"] = cotime
in_param["adult_num"] = "2"
in_param["children"] = ""
in_param["search_id"] = "123456789"
in_param["elong_pid"] = elong_pid
in_param["ota_sign"] = ota_sign
in_param["room_num"] = "2"
in_param["show_type"] = "1"
in_param_json = json.dumps(in_param)
in_param_dict = json.loads(in_param_json)
bk_rlt = booking(in_param_json)
bk_jrlt = json.loads(bk_rlt)
if bk_jrlt['service_status']['msg'] == 'success' :
    print "########## booking response success"
if bk_jrlt['booking_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['promotion_info'][0]['type'] == 7 :
    print "########## promotion info success"