#!/usr/bin/env python
#-*- coding: utf-8 -*-
from gen import price_types_pb2
from gen import as_types_pb2
from gen import price_service_pb2
import json
from pbTojson.pbjson import pb2json, pb2dict


def response(serialized_msg, show_type):
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
