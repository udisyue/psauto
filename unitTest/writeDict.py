import os
import time
import re
import json

def fileRplace(fname):
    bak_file = fname+'.bak'
    cp_command = 'cp '+fname+' '+bak_file
    rm_command = 'rm -f '+fname
    os.system(cp_command)
    os.system(rm_command)

def autoPriceRule_write(hotelid,chnlid,time,discount,ruleid):
    fo = open('/home/work/idata/price/dict/base/auto_price_rule.dict', 'wb')
    content = str(hotelid)+'\t'+str(chnlid)+'\t'+str(time)+'\t'+str(discount)+'\t'+str(ruleid)
    fo.write(content)
    fo.close()
    os.system('touch /home/work/idata/price/done')

def fileRecov(fname):
    bak_file = fname+'.bak'
    cp_command = 'rm -f '+fname
    rm_command = 'cp '+fname+' '+bak_file
    os.system(rm_command)
    os.system(cp_command)
    os.system('touch /home/work/idata/price/done')

def manualPrice_write(hotelid):
    fo = open('/home/work/idata/price/dict/base/manual_price_tool.dict','wb')
    content = '*\t*\t*\t*\t*\t[{"ci_end_time": 1798473600, "oid": 13, "end_time": 1608825600, "begin_time": 1482076800, "ci_begin_time": 1482163200, "op": {"op_code": "*", "op_val": 0.94999999999999996}}]'
    fo.write(content)
    fo.close()
    os.system('touch /home/work/idata/price/done')
    
def autoPriceInfo_write(lbflag,borc,borm):
    if lbflag == 0:
        if borc == 1 and borm == 1:
            info = '55\t{"booking_time_end": 1514735999, "modify_otas": [6, 7, 8, 5, 10, 11, 13, 12, 14, 15, -1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 2, 27, 28], "booking_time_start": 1497283200, "lose_info": {"lose_copy_price": {"H": 1.0, "C": 0}, "lose_copy_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_modify_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_tags": "", "lose_base_or_copy": 1, "lose_base_or_modify": 1, "lose_modify_price": {"H": 1.0, "C": 0}}, "booking_channel": [2, 32, 16, 256], "copy_otas": [], "copy_cnt": 1}'
        elif borc == 1 and borm == 2:
            info = '55\t{"booking_time_end": 1514735999, "modify_otas": [6, 7, 8, 5, 10, 11, 13, 12, 14, 15, -1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 2, 27, 28], "booking_time_start": 1497283200, "lose_info": {"lose_copy_price": {"H": 1.0, "C": 0}, "lose_copy_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_modify_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_tags": "", "lose_base_or_copy": 1, "lose_base_or_modify": 2, "lose_modify_price": {"H": 1.0, "C": 0}}, "booking_channel": [2, 32, 16, 256], "copy_otas": [], "copy_cnt": 1}'
        elif borc == 2 and borm == 1:
            info = '55\t{"booking_time_end": 1514735999, "modify_otas": [6, 7, 8, 5, 10, 11, 13, 12, 14, 15, -1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 2, 27, 28], "booking_time_start": 1497283200, "lose_info": {"lose_copy_price": {"H": 1.0, "C": 0}, "lose_copy_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_modify_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_tags": "", "lose_base_or_copy": 2, "lose_base_or_modify": 1, "lose_modify_price": {"H": 1.0, "C": 0}}, "booking_channel": [2, 32, 16, 256], "copy_otas": [3], "copy_cnt": 1}'
        elif borc == 2 and borm == 2:
            info = '55\t{"booking_time_end": 1514735999, "modify_otas": [6, 7, 8, 5, 10, 11, 13, 12, 14, 15, -1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 2, 27, 28], "booking_time_start": 1497283200, "lose_info": {"lose_copy_price": {"H": 1.0, "C": 0}, "lose_copy_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_modify_base_price": {"E": 0, "F": 0.029999999999999999}, "lose_tags": "", "lose_base_or_copy": 2, "lose_base_or_modify": 2, "lose_modify_price": {"H": 1.0, "C": 0}}, "booking_channel": [2, 32, 16, 256], "copy_otas": [3], "copy_cnt": 1}'
        fo = open('/home/work/idata/price/dict/base/auto_price_info.dict', 'wb')
        fo.write(info)
        fo.close()
        os.system('touch /home/work/idata/price/done')
    else:
        info = '55\t{"booking_time_end": 1514735999, "modify_otas": [2, 6, 7, 8, 5, 9, 10, 11, 13, 1, 12, 3, 14, 15, -1, 16, 17, 18, 19, 20, 24, 25, 26, 27, 28], "booking_time_start": 1489507200, "tts_QT": 900, "tts_QP": 0.20000000000000001, "booking_channel": [2, 32, 16, 256], "beat_info": {"beat_copy_list": [{"H": 0.90000000000000002, "C": 900}, {"H": 0.90000000000000002, "C": 0}], "beat_modify_price": {"H": 0.90000000000000002, "C": 900}, "beat_tags": ""}, "copy_otas": [], "copy_cnt": 2}'
        fo = open('/home/work/idata/price/dict/base/auto_price_info.dict', 'wb')
        fo.write(info)
        fo.close()
        os.system('touch /home/work/idata/price/done')

def ruleBlack_write(hotelid,ota,flag):
    fo = open('/home/work/idata/price/dict/base/rule_blacklist.dict', 'a')
    content = str(hotelid) + '\t' + str(ota) + '\t' + str(flag)
    fo.write(content)
    fo.close()

