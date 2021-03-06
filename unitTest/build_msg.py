#!/usr/bin/env python
#-*- coding: utf-8 -*-
from gen import price_types_pb2
from gen import as_types_pb2
from gen import price_service_pb2

import time
def request_list(nshead, in_param_dict, coupon_switch):
    # get param
    try:
        booking_channel = 0 if in_param_dict["booking_channel"] == '' else int(in_param_dict["booking_channel"])
        order_from = 0 if in_param_dict["order_from"] == '' else int(in_param_dict["order_from"])
        customer_level = 0 if in_param_dict["customer_level"] == '' else int(in_param_dict["customer_level"])
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
    request.user_info.customer_level = customer_level
    request.user_info.order_from = order_from
    request.user_info.booking_channel = booking_channel
    # coupon info
    if coupon_switch :
        request.user_info.activity_id_list.append(2015081441);
        request.user_info.activity_id_list.append(2015081432);
        request.user_info.activity_id_list.append(2015081457);
        request.user_info.activity_id_list.append(2015081452);
        request.user_info.activity_id_list.append(2017000064);
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

#*****************************************************************************************#

def request_detail(nshead, in_param_dict):
    # get param
    try:
        booking_channel = 0 if in_param_dict["booking_channel"] == '' else int(in_param_dict["booking_channel"])
        order_from = 0 if in_param_dict["order_from"] == '' else int(in_param_dict["order_from"])
        customer_level = 0 if in_param_dict["customer_level"] == '' else int(in_param_dict["customer_level"])
        # user_ip = in_param_dict["user_ip"]
        hotel_id = in_param_dict["hotel_id"]
        filter_ota = 0 if in_param_dict["filter_ota"] == '' else int(in_param_dict["filter_ota"])
        checkin = '2018-1-1' if in_param_dict["checkin"] == '' else in_param_dict["checkin"]
        checkout = '2018-1-2' if in_param_dict["checkout"] == '' else in_param_dict["checkout"]
        adult_num = 0 if in_param_dict["adult_num"] == '' else int(in_param_dict["adult_num"])
        children = in_param_dict["children"]
        search_id = in_param_dict["search_id"]
        activity_id = in_param_dict["activity_id"]
    except Exception as e:
        print e
        return "", 0

    request = price_service_pb2.PsRequest()
    # search_id
    request.search_id = search_id;
    # version_id
    request.version_id = 2
    # user_info
    request.user_info.user_ip = "127.0.0.1"
    request.user_info.customer_level = customer_level
    request.user_info.order_from = order_from
    request.user_info.booking_channel = booking_channel
    # coupon info
    # request.user_info.activity_id_list.append(1);
    # request.user_info.activity_id_list.append(2);
    # request.user_info.activity_id_list.append(3);
    # request.user_info.activity_id_list.append(4);
    for ai in activity_id.split(','):
        if ai != '':
            request.user_info.activity_id_list.append(int(ai))
    # search_type
    request.service_type = 2
    # detail_req - query_info
    # request.detail_request.query_info.region_id = 178308
    for hid in hotel_id.split(','):
        if hid != '':
            request.detail_request.query_info.hotel_id.append(int(hid))
    request.detail_request.query_info.filter_ota = filter_ota
    # request.detail_request.query_info.cache_time = 1000
    # request.detail_request.query_info.timeout = 3000
    request.detail_request.query_info.cashpay_booking_channel_mask = 0
    room = request.detail_request.query_info.room_person.add()
    room.adult_num = adult_num
    for c in children.split(','):
        if c != '':
            room.child_age_list.append(int(c))
    timeArray = time.strptime(checkin, "%Y-%m-%d")
    request.detail_request.query_info.check_in_date = int(time.mktime(timeArray)) + 1000
    timeArray = time.strptime(checkout, "%Y-%m-%d")
    request.detail_request.query_info.check_out_date = int(time.mktime(timeArray)) + 1000

    return request.SerializeToString(), request.ByteSize()

#*****************************************************************************************#
