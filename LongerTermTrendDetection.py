# LongerTermTrendDetection.py
# Patrick Neary
# 11/30/2015
#
# Description: Code to detect long and short term trend detection.  Right now this will only detect the long term
# trend (bullish/bearish) and mid term trend (bullish bearish).  There isn't anything right now for detecting flat
# markets or whipsaws.  Hopefully that will come soon.  This code will use the 200 SMA so, enough history needs to be
# present to calculate those values.  Assume that stochastics and MAs are calculated somewhere else.
#
# I want to make this pretty self contained.
# bullish = 1
# bearish = 2
# whipsaw = 4



def GetTrends(sma50, sma200, stoch50, stoch20, shorttermtrend):
    # This function will return the long term trend as well as the mid/short term trend.
    # shorttermtrend is what the current detected trend is.
    longTermTrend = -1
    shortTermTrend = shorttermtrend

    #slowstoch50 = stoch50[1]
    faststoch50 = stoch50[0]
    faststoch20 = stoch20[0]

    if(sma50[-1] < sma200[-1]): longTermTrend = 2    # Bearish
    elif(sma50[-1] >= sma200[-1]): longTermTrend = 1 # Bullish

    # Detect a whipsaw condition
    if((faststoch20[-1] > 25) and (faststoch20[-1] < 75)):
        if((faststoch20[-3] >= faststoch20[-2]) and (faststoch20[-1] > faststoch20[-2])): # Curled upward
            shortTermTrend = 4
        elif((faststoch20[-3] <= faststoch20[-2]) and (faststoch20[-1] < faststoch20[-2])): # Curled downward
            shortTermTrend = 4

    # Look at Bullish trend and detect short term trends
    if(longTermTrend == 1):
        if((faststoch50[-2] >= 75) and (faststoch50[-1] < 75)): # We've transitioned from short to long
            shortTermTrend = 2

        elif(faststoch50[-1] > 75):
            shortTermTrend = 1

        elif(faststoch50[-1] < 75):
            if((faststoch50[-3] > faststoch50[-2]) and (faststoch50[-1] > faststoch50[-2])): # Curled upward
                shortTermTrend = 1
            elif((faststoch50[-3] < faststoch50[-2]) and (faststoch50[-1] < faststoch50[-2])): # Curled downward
                shortTermTrend = 2

    # Look at long term bearish trend and detect short term trends
    elif(longTermTrend == 2):
        if((faststoch50[-2] <= 25) and (faststoch50[-1] > 25)): # We've transitioned from short to long
            shortTermTrend = 1

        elif(faststoch50[-1] < 25):
            shortTermTrend = 2

        elif(faststoch50[-1] > 25):
            if((faststoch50[-3] > faststoch50[-2]) and (faststoch50[-1] > faststoch50[-2])): # Curled upward
                shortTermTrend = 1
            elif((faststoch50[-3] < faststoch50[-2]) and (faststoch50[-1] < faststoch50[-2])): # Curled downward
                shortTermTrend = 2

    return longTermTrend, shortTermTrend


