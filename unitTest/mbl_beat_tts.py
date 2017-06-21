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
import writeDict
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

citime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
cotime = time.strftime('%Y-%m-%d',time.localtime(time.time()+86400))
cur_time = re.sub(r'-', "", citime)
offset = 0
writeDict.fileRplace('/home/work/idata/price/dict/base/auto_price_rule.dict')
writeDict.fileRplace('/home/work/idata/price/dict/base/auto_price_info.dict')
writeDict.autoPriceInfo_write(1, 1, 1)
writeDict.autoPriceRule_write(324743,256,cur_time,1.2,55)

offset, rule = readDict.readAPRule(offset, cur_time)
if offset != 0 :
    # set param
    in_param = {}
    # in_param["ip"] = "192.168.14.170"
    in_param["ip"] = "192.168.232.40"
    in_param["port"] = "6300"
    in_param["booking_channel"] = rule[1]
    in_param["order_from"] = "50"
    in_param["customer_level"] = "1"
    # in_param["user_ip"] = "127.0.0.1"
    in_param["hotel_id"] = 324743
    in_param["filter_ota"] = "524286"

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
    info = readDict.readAPInfo(rule[4])


    rlt = detail(in_param_json)
    jrlt = json.loads(rlt)
    if jrlt['service_status']['msg'] == 'success' and jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['hotel_status']==2:
        b_s_price = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['base_sale_price']['total_price']['amount']
        ori_price = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['origin_price']['total_price']['amount']
        ota = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['ota_id']
        # mbl parse
        base = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['base_price']['total_price']['amount']
        cost = jrlt['detail_response']['detail_hotel']['detail_ota_list'][0]['room_list'][0]['product_list'][0]['cost_price']['total_price']['amount']
        rate = (base - cost) / base
        b = float(rule[3])
        if b > 1 :
            h_beat = [info['beat_info']['beat_copy_list'][0]['H'], info[1]['beat_info']['beat_copy_list'][1]['H'], info[1]['beat_info']['beat_modify_price']['H']]
            c_beat = [info['beat_info']['beat_copy_list'][0]['C'], info[1]['beat_info']['beat_copy_list'][1]['C'], info[1]['beat_info']['beat_modify_price']['C']]
            if int(rule[1]) == 256 and info['beat_info']['tts_QT']:
                qt = info['beat_info']['tts_QT']
                qp = info['beat_info']['tts_QP']
            else :
                qt = 0
                qp = 0
            copy_price1, copy_price2, modify_price, cp1_tts, cp2_tts, mprice=mbl_math.beat(base, b, h_beat, c_beat, qt, qp)
            if modify_price < base :
                if b_s_price == modify_price:
                    print '#####base sale price = modify  price, auto price success'
                else:
                    print '#####base sale price != modify price, auto price failed'

        else :
            h_lose = [info['lose_info']['lose_copy_price']['H'], info['lose_info']['lose_modify_price']['H']]
            c_lose = [info['lose_info']['lose_copy_price']['C'], info['lose_info']['lose_modify_price']['C']]
            f_lose = [info['lose_info']['lose_copy_base_price']['F'], info['lose_info']['lose_modify_base_price']['F']]
            e_lose = [info['lose_info']['lose_copy_base_price']['E'], info['lose_info']['lose_modify_base_price']['E']]
            if int(rule[1]) == 256:
                qt = info['lose_info']['tts_QT']
                qp = info['lose_info']['tts_QP']
            else :
                qt = 0
                qp = 0
            copy_base, copy_price, modify_base, modify_price, copybase_tts, copyprice_tts, mbase_tts, mprice_tts=mbl_math.lose(base, b, h_lose, c_lose, f_lose, e_lose, rate, qt, qp)
            if modify_price < base :
                if b_s_price == modify_price:
                    print '#####base sale price = modify  price, auto price success'
                else:
                    print '#####base sale price != modify price, auto price failed'