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


# be care : update接口只支持一供应商多酒店的更新；不支持多供应商更新！
# 该脚本支持一供应商一酒店更新

def build_message(nshead, in_param_dict):
    # get param
    try:
        hotel_id = int(in_param_dict["hotel_id"])
        otaid = int(in_param_dict["otaid"])
        checkin = '2018-1-1' if in_param_dict["checkin"] == '' else in_param_dict["checkin"]
        checkout = '2018-1-2' if in_param_dict["checkout"] == '' else in_param_dict["checkout"]
        booking_channel = 0 if in_param_dict["booking_channel"] == '' else int(in_param_dict["booking_channel"])
        adult_num = 0 if in_param_dict["adult_num"] == '' else int(in_param_dict["adult_num"])
        search_id = in_param_dict["search_id"]
        children = in_param_dict["children"]
        list_only = False if in_param_dict["list_only"] == '0' else True
        hotel_status = int(in_param_dict["hotel_status"])
        # room1
        room1 = False if in_param_dict["room1"] == '0' else True
        roomId1 = long(in_param_dict["roomId1"])
        roomNameCn1 = in_param_dict["roomNameCn1"].encode('utf-8')
        roomStatus1 = int(in_param_dict["roomStatus1"])
        
        # product11
        product11 = False if in_param_dict["product11"] == '0' else True
        elongPid11 = long(in_param_dict["elongPid11"])
        productNameCn11 = in_param_dict["productNameCn11"].encode('utf-8')
        mobile11 = 0 if in_param_dict["mobile11"] == '0' else 1
        cashPay11 = 1 if in_param_dict["cashPay11"] == '0' else 2
        averRoomPrice11 = long(in_param_dict["averRoomPrice11"])
        averPrice11 = long(in_param_dict["averPrice11"])
        
        # product12
        product12 = False if in_param_dict["product12"] == '0' else True
        elongPid12 = long(in_param_dict["elongPid12"])
        productNameCn12 = in_param_dict["productNameCn12"].encode('utf-8')
        mobile12 = 0 if in_param_dict["mobile12"] == '0' else 1
        cashPay12 = 1 if in_param_dict["cashPay12"] == '0' else 2
        averRoomPrice12 = long(in_param_dict["averRoomPrice12"])
        averPrice12 = long(in_param_dict["averPrice12"])
        
        # room2
        room2 = False if in_param_dict["room2"] == '0' else True
        roomId2 = long(in_param_dict["roomId2"])
        roomNameCn2 = in_param_dict["roomNameCn2"].encode('utf-8')
        roomStatus2 = int(in_param_dict["roomStatus2"])
        
        # product21
        product21 = False if in_param_dict["product21"] == '0' else True
        elongPid21 = long(in_param_dict["elongPid21"])
        productNameCn21 = in_param_dict["productNameCn21"].encode('utf-8')
        mobile21 = 0 if in_param_dict["mobile21"] == '0' else 1
        cashPay21 = 1 if in_param_dict["cashPay21"] == '0' else 2
        averRoomPrice21 = long(in_param_dict["averRoomPrice21"])
        averPrice21 = long(in_param_dict["averPrice21"])
        
        # product22
        product22 = False if in_param_dict["product22"] == '0' else True
        elongPid22 = long(in_param_dict["elongPid22"])
        productNameCn22 = in_param_dict["productNameCn22"].encode('utf-8')
        mobile22 = 0 if in_param_dict["mobile22"] == '0' else 1
        cashPay22 = 1 if in_param_dict["cashPay22"] == '0' else 2
        averRoomPrice22 = long(in_param_dict["averRoomPrice22"])
        averPrice22 = long(in_param_dict["averPrice22"])
        
    except Exception as e:
        # print e
        return "", 0
        
        
    request = price_service_pb2.PsRequest()
    # search_id
    request.search_id = search_id; 
    # version_id
    request.version_id = 1
    # user_info
    request.user_info.user_ip = "192.168.21.1"
    request.user_info.customer_level = 2
    request.user_info.order_from = 2
    request.user_info.booking_channel = booking_channel
    # search_type
    request.service_type = 4
    # update_req - query_info
    request.price_update_request.query_info.hotel_id.append(hotel_id)
    room = request.price_update_request.query_info.room_person.add()
    room.adult_num  = 2
    # room1 = request.price_update_request.query_info.room_person.add()
    # room1.adult_num  = 2
    #room.child_ages = "10"
    for c in children.split(','):
        if c != '':
            room.child_age_list.append(int(c))
    timeArray = time.strptime(checkin, "%Y-%m-%d")
    request.price_update_request.query_info.check_in_date = int(time.mktime(timeArray)) + 1000
    timeArray = time.strptime(checkout, "%Y-%m-%d")
    request.price_update_request.query_info.check_out_date = int(time.mktime(timeArray)) + 1000

    # update_list_only
    request.price_update_request.query_info.update_list_only = list_only
    
    # DetailOta - 1
    detail_ota1 = request.price_update_request.detail_ota.add()
    detail_ota1.base_hotel_id = hotel_id
    detail_ota1.ota_id = otaid
    detail_ota1.hotel_status = hotel_status # 2-SUCCESS_STOCK
    detail_ota1.crawl_time = int(time.time())
    # room - 1
    if room1:
        croom1 = detail_ota1.room_list.add()
        croom1.room_id = roomId1
        croom1.room_name_cn = roomNameCn1
        croom1.room_status = roomStatus1  # 1-open

        # product - 1.1
        if product11:
            cproduct11 = croom1.product_list.add()
            cproduct11.elong_pid = elongPid11
            cproduct11.product_name_cn = productNameCn11
            cproduct11.room_num = 3
            cproduct11.rateplan.ota_promo_type = mobile11          # 1-手机专享; 0-非手机专享    
            cproduct11.rateplan.pay_type = cashPay11               # 1-预付; 2-现付 
            # origin_price(分)
            cproduct11.origin_price.average_room_price.amount = averRoomPrice11
            cproduct11.origin_price.average_room_price.currency = "CNY"
            cproduct11.origin_price.average_price.amount = averPrice11
            cproduct11.origin_price.average_price.currency = "CNY"
        
        # product - 1.2
        if product12:
            cproduct12 = croom1.product_list.add()
            cproduct12.elong_pid = elongPid12
            cproduct12.product_name_cn = productNameCn12
            cproduct12.room_num = 3
            cproduct12.rateplan.ota_promo_type = mobile12          # 1-手机专享; 0-非手机专享
            cproduct12.rateplan.pay_type = cashPay12               # 1-预付; 2-现付 
            # origin_price(分)
            cproduct12.origin_price.average_room_price.amount = averRoomPrice12
            cproduct12.origin_price.average_room_price.currency = "CNY"
            cproduct12.origin_price.average_price.amount = averPrice12
            cproduct12.origin_price.average_price.currency = "CNY"
    
    
    # room - 2
    if room2:
        croom2 = detail_ota1.room_list.add()
        croom2.room_id = roomId2
        croom2.room_name_cn = roomNameCn2
        croom2.room_status = roomStatus2 # 1-open

        # product - 2.1
        if product21:
            cproduct21 = croom2.product_list.add()
            cproduct21.elong_pid = elongPid21
            cproduct21.product_name_cn = productNameCn21
            cproduct21.room_num = 3
            cproduct21.rateplan.ota_promo_type = mobile21          # 1-手机专享; 0-非手机专享    
            cproduct21.rateplan.pay_type = cashPay21               # 1-预付; 2-现付 
            # origin_price(分)
            cproduct21.origin_price.average_room_price.amount = averRoomPrice21
            cproduct21.origin_price.average_room_price.currency = "CNY"
            cproduct21.origin_price.average_price.amount = averPrice21
            cproduct21.origin_price.average_price.currency = "CNY"
        
        # product - 2.2
        if product22:
            cproduct22 = croom2.product_list.add()
            cproduct22.elong_pid = elongPid22
            cproduct22.product_name_cn = productNameCn22
            cproduct22.room_num = 3
            cproduct22.rateplan.ota_promo_type = mobile22          # 1-手机专享; 0-非手机专享
            cproduct22.rateplan.pay_type = cashPay22               # 1-预付; 2-现付 
            # origin_price(分)
            cproduct22.origin_price.average_room_price.amount = averRoomPrice22
            cproduct22.origin_price.average_room_price.currency = "CNY"
            cproduct22.origin_price.average_price.amount = averPrice22
            cproduct22.origin_price.average_price.currency = "CNY"


    return request.SerializeToString(), request.ByteSize()

def handle_response(serialized_msg):
    response = price_service_pb2.PsResponse()
    response.ParseFromString(serialized_msg)
    # text_format.PrintMessage(response, sys.stdout)
    # return response
    # response_str = text_format.MessageToString(response)
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
                  
                response = handle_response(serialized_msg)
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
            in_param["hotel_id"] = "324748"
            in_param["otaid"] = 13
            in_param["checkin"] = "2016-10-10"
            in_param["checkout"] = "2016-10-11"
            in_param["booking_channel"] = 2
            in_param["adult_num"] = 2 
            in_param["search_id"] = "123456789"
            in_param["children"] = ""
            in_param["list_only"] = '0'
            in_param["hotel_status"] = 2
            # room1
            in_param["room1"] = '1'  # 1-on 2-off
            in_param["roomId1"] = "234"
            in_param["roomNameCn1"] = "roomNameCn1"
            in_param["roomStatus1"] = '1' 

            # product11
            in_param["product11"] = '1' 
            in_param["elongPid11"] = '34613405'
            in_param["productNameCn11"] = "productNameCn11"
            in_param["mobile11"] = '1'
            in_param["cashPay11"] = '0'
            in_param["averRoomPrice11"] = "3745"
            in_param["averPrice11"] = "4987"
            
            # product12
            in_param["product12"] = '1'
            in_param["elongPid12"] = "4562045602"
            in_param["productNameCn12"] = "productNameCn12"
            in_param["mobile12"] = '0'
            in_param["cashPay12"] = '1'
            in_param["averRoomPrice12"] = "5654"
            in_param["averPrice12"] = "5699"
 
            # room2
            in_param["room2"] = '1'  # 1-on 2-off
            in_param["roomId2"] = "234"
            in_param["roomNameCn2"] = "roomNameCn2"
            in_param["roomStatus2"] = '1' 

            # product21
            in_param["product21"] = '1' 
            in_param["elongPid21"] = '34613405'
            in_param["productNameCn21"] = "productNameCn21"
            in_param["mobile21"] = '1'
            in_param["cashPay21"] = '0'
            in_param["averRoomPrice21"] = "3745"
            in_param["averPrice21"] = "4987"
            
            # product22
            in_param["product22"] = '1'
            in_param["elongPid22"] = "4562045602"
            in_param["productNameCn22"] = "productNameCn22"
            in_param["mobile22"] = '0'
            in_param["cashPay22"] = '1'
            in_param["averRoomPrice22"] = "5654"
            in_param["averPrice22"] = "5699"


            # print "origin: ", type(in_param)
            in_param_json = json.dumps(in_param)
            # print "dict 2 json: ", type(in_param_json)
            in_param_dict = json.loads(in_param_json)
            # print "json 2 dict: ", type(in_param_dict)
            time1 = time.time()
            print main(in_param_json)
            time2 = time.time()
            print "use time : ", time2-time1
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logging.error(e)
            raise
