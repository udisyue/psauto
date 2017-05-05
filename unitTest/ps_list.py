#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append("./script/unitTest")
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


def build_message(nshead, in_param_dict):
    # get param
    try:
        booking_channel = 0 if in_param_dict["booking_channel"] == '' else int(in_param_dict["booking_channel"])
        # order_from = 0 if in_param_dict["order_from"] == '' else int(in_param_dict["order_from"])
        # customer_level = 0 if in_param_dict["customer_level"] == '' else int(in_param_dict["customer_level"])
        # user_ip = in_param_dict["user_ip"]
        hotel_id = in_param_dict["hotel_id"]
        filter_ota = 0 if in_param_dict["filter_ota"] == '' else int(in_param_dict["filter_ota"])
        checkin = '2018-1-1' if in_param_dict["checkin"] == '' else in_param_dict["checkin"]
        checkout = '2018-1-2' if in_param_dict["checkout"] == '' else in_param_dict["checkout"]
        adult_num = 0 if in_param_dict["adult_num"] == '' else int(in_param_dict["adult_num"])
        children = in_param_dict["children"]
        search_id = in_param_dict["search_id"]
        list_query_flag = 0 if in_param_dict["list_query_flag"] == '' else int(in_param_dict["list_query_flag"])
        activity_id = in_param_dict["activity_id"]
        user_id = in_param_dict["user_id"]
    except Exception as e:
        print e
        return "", 0

    request = price_service_pb2.PsRequest()
    # search_type
    request.service_type = 1
    # search_id
    request.search_id = search_id; 
    # version_id
    request.version_id = 2
    # user_info
    request.user_info.user_ip = "127.0.0.1"
    # request.user_info.customer_level = customer_level
    # request.user_info.order_from = order_from
    request.user_info.booking_channel = booking_channel
    request.user_info.user_id = user_id
    # coupon info
    #request.user_info.activity_id_list.append(2015081441);
    #request.user_info.activity_id_list.append(2015081432);
    #request.user_info.activity_id_list.append(2015081457);
    #request.user_info.activity_id_list.append(2015081452);
    # detail_req - query_info
    # request.list_request.query_info.region_id = 178308
    for ai in activity_id.split(','):
        if ai != '':
            request.user_info.activity_id_list.append(int(ai))
    for hid in hotel_id.split(','):
        if hid != '':
            request.list_request.query_info.hotel_id.append(int(hid))
    request.list_request.query_info.filter_ota = filter_ota
    request.list_request.query_info.cashpay_booking_channel_mask = 0
    room = request.list_request.query_info.room_person.add()
    room.adult_num  = adult_num
    for c in children.split(','):
        if c != '':
            room.child_age_list.append(int(c))
    timeArray = time.strptime(checkin, "%Y-%m-%d")
    request.list_request.query_info.check_in_date = int(time.mktime(timeArray)) + 1000
    timeArray = time.strptime(checkout, "%Y-%m-%d")
    request.list_request.query_info.check_out_date = int(time.mktime(timeArray)) + 1000
    # list_query_flag
    # as请求ps可能的参数:
    # 3  0011 : ORIGIN_PRICE | ELONG_PRICE  - 列表页批量接口
    # 15 1111 : ORIGIN_PRICE | ELONG_PRICE | PROMOTION | DIGEST - 列表页批量接口
    # 1  0001 : ORIGIN_PRICE  - 列表页检索接口
    # 7  0111 : ORIGIN_PRICE | ELONG_PRICE | PROMOTION - 列表页检索接口
    request.list_request.query_info.list_query_flag = list_query_flag
    
    return request.SerializeToString(), request.ByteSize()

def handle_response(serialized_msg, show_type):
    response = price_service_pb2.PsResponse()
    response.ParseFromString(serialized_msg)
    # text_format.PrintMessage(response, sys.stdout)
    # return response
    # response_str = text_format.MessageToString(response)
   
    if  show_type == "1":
        # return pb2json(response)
        return json.dumps(json.loads(pb2json(response)), indent=4, sort_keys=False, ensure_ascii=False)
    else:
        return pb2dict(response)

# in_param must be json!
def main(in_param):
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
        msg, length = build_message(nshead, in_param_dict)
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
    

if __name__ == '__main__':
        try:
            # set param
            in_param = {}
            in_param["ip"] = "192.168.14.170"
            in_param["port"] = "6300"
            in_param["booking_channel"] = "2"
            # in_param["order_from"] = "0"
            # in_param["customer_level"] = "0"
            # in_param["user_ip"] = "127.0.0.1"
            in_param["user_id"] = ""
            in_param["hotel_id"] = "442586"
            in_param["filter_ota"] = "512"
            in_param["checkin"] = "2016-12-15"
            in_param["checkout"] = "2016-12-16"
            in_param["adult_num"] = "2"
            in_param["children"] = ""
            in_param["search_id"] = "123456789"
            in_param["list_query_flag"] = "7"
            # in_param["list_query_flag"] = "1"  # 只要原始价
            in_param["show_type"] = "1"
            # in_param["activity_id"] = "2015081441,2015081442"
            in_param["activity_id"] = ""
            # print "origin: ", type(in_param)
            in_param_json = json.dumps(in_param)
            # print "dict 2 json: ", type(in_param_json)
            in_param_dict = json.loads(in_param_json)
            # print "json 2 dict: ", type(in_param_dict)
            time1 = time.time()
            print main(in_param_json)
            time2 = time.time()
            # print "use time : ", time2-time1
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logging.error(e)
            raise
