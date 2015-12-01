# CandlestickTools.py
# Patrick Neary
# 11/25/2015
#
# Description:  Tools for working with candlesticks


import numpy
import talib


def GetCandleBodyLen(openp, closep):
    candlelen = max(openp, closep) - min(openp, closep)
    return candlelen


def IsDoji(openp, highp, lowp, closep):
    isdoji = 0

    # Doji ratios
    oc = abs(openp-closep)
    hl = abs(highp-lowp)*0.3

    if(oc <= hl):
        isdoji = 1

    return isdoji

