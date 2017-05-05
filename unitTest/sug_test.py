#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import json
sys.path.append("./script/unitTest")

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

    return in_param_dict

if __name__ == "__main__":
    in_param = {}
    in_param["input_str"] = "192.168.14.170"
    print main(in_param)
