#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
#Import Custom ackage
import build_msg
import log_write
import handle_response

#static config
if_log_on = 1
if_coupon_on = 1


