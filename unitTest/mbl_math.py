#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

def beat(base, b, h_beat, c_beat, qt, qp) :
    copy_price1 = base * b * h_beat[0] - c_beat[0]
    copy_price2 = base * b * h_beat[1]
    modify_price = base * b * h_beat[2] - c_beat[2]
    print ("hit beat")
    print ("copy_price1 = %f"%copy_price1)
    print ("copy_price2 = %f"%copy_price2)
    print ("modify_price = %f"%modify_price)
    cp1_tts = copy_price1 * (1 + qt) + qp
    cp2_tts = copy_price2 * (1 + qt) + qp
    mprice = modify_price * (1 + qt) + qp
    print ("copy_price1_tts = %f" % cp1_tts)
    print ("copy_price2_tts = %f" % cp2_tts)
    print ("modify_price_tts = %f" % mprice)
    return copy_price1, copy_price2, modify_price, cp1_tts, cp2_tts, mprice

def lose(base, b, h_lose, c_lose, f_lose, e_lose, rate, qt, qp) :
    copy_base = base * (1 - rate) * (1 + f_lose[0]) + e_lose[0]
    copy_price = base * b * h_lose[0] - c_lose[0]
    modify_base = base * (1 - rate) * (1 + f_lose[1]) + e_lose[1]
    modify_price = base * b * h_lose[1] - c_lose[1]
    copybase_tts = copy_base * (1 + qt) + qp
    copyprice_tts = copy_price * (1 + qt) + qp
    mbase_tts = modify_base * (1 + qt) + qp
    mprice_tts = modify_price * (1 + qt) + qp
    print ("hit lose")
    print ("copy_base =  %f"%copy_base)
    print ("copy_price = %f"%copy_price)
    print ("modify_base = %f"%modify_base)
    print ("modify_price = %f"%modify_price)
    print ("copy_base_tts =  %f"%copybase_tts)
    print ("copy_price_tts = %f"%copyprice_tts)
    print ("modify_base_tts = %f"%mbase_tts)
    print ("modify_price_tts = %f"%mprice_tts)
    return copy_base, copy_price, modify_base, modify_price, copybase_tts, copyprice_tts, mbase_tts, mprice_tts

def main():
    base = 32702
    b = 0.961
    h_beat = [0.80000000000000001,0.80000000000000001,0.90000000000000002]
    c_beat = [900,0,900]
    h_lose = [0.8,0.8]
    c_lose = [0,0]
    f_lose = [0.0,0.05]
    e_lose = [0,0]
    f = 0.02
    e  = 0
    cost = 27681
    qt = 0.19
    qp = 10000
    rate = (base - cost) / base
    if b > 1 :
        beat(base, b, h_beat, c_beat, qt, qp)
    else :
        lose(base, b, h_lose, c_lose, f_lose, e_lose, rate, qt, qp)

if __name__ == '__main__':
    main()
