# IndicatorTools.py
# Patrick Neary
# 11/23/2015
#
# Description:  Tools for getting indicator data for a given security


import numpy
import talib


def GetADXValues(secdata):
    # secdata contains data acquired from google/yahoo packages
    val = talib.ADX(numpy.asarray(secdata['High']), numpy.asarray(secdata['Low']), numpy.asarray(secdata['Close']), 14)
    return val


def GetADXValues2(highd, lowd, closed):
    # secdata contains data acquired from google/yahoo packages
    val = talib.ADX(numpy.asarray(highd), numpy.asarray(lowd), numpy.asarray(closed), 14)
    return val


def GetStochValues(highd, lowd, closed, Length, D, K):
    #it.GetStochValues(tickerdata['High'], tickerdata['Low'], tickerdata['Close'], 20, 5, 5)
    # Get stochastic data for the included set of data.
    # D is the slower line and K is the faster.
    stoch = talib.STOCH(numpy.asarray(highd), numpy.asarray(lowd), numpy.asarray(closed), fastk_period=Length,
                            slowk_period=K, slowd_period=D)

    return stoch


def GetSMAValues(inputp, period):
    #it.GetSMAValues(tickerdata['Close'], 50)
    # Get SMA data for the supplied data at the specified period

    sma = talib.SMA(numpy.asarray(inputp), timeperiod=period)

    return sma

