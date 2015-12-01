# TrendStateTransition.py
# Patrick Neary
# 11/23/2015
#
# Description: Code handling the logic allowing flow between market states:
# bullish, bearish, whipsaw, ranging, unknown

import IndicatorTools as it
import RegressionTools as rt
import CandlestickTools as ct
import LongerTermTrendDetection as ltd
import numpy


class TransitionState:

    def __init__(self, emaPeriod=10, mse=5e-3):
        # ema period is for the smoothing function applied to the security data prior to running regression
        # mse is the desired mean squared error at which to stop looping through the nonlinear regression
        self.emaPeriod = emaPeriod
        self.mse = mse

        self.candleAvgLen = 0
        self.candleStdDev = 0

        self.unknown = 0
        self.bullish = 1
        self.bearish = 2
        self.range = 3
        self.whipsaw = 4
        self.state = self.unknown

        self.maxSize = 800 # Maximum size of lists.  No need to have more than this that I can see right now
        self.dataCnt = 0
        self.smoothed = []
        self.avgd = []
        self.open = []
        self.close = []
        self.high = []
        self.low = []
        self.regResults = []
        self.dates = []
        self.midtrend = 0

        return


    def GetState(self,):
        if(self.state == self.unknown): return 'Unknown', 0
        elif(self.state == self.bullish): return 'Bullish', 1
        elif(self.state == self.bearish): return 'Bearish', 2
        elif(self.state == self.range): return 'Range', 3
        elif(self.state == self.whipsaw): return 'Whipsaw', 4

        return 'Unknown', 0


    def PopCandle(self):
        # Remove one data entry from structures so we don't exceed specified size limit
        self.avgd.popleft()
        #self.smoothed.popleft()
        self.open.popleft()
        self.close.popleft()
        self.high.popleft()
        self.low.popleft()
        self.dates.popleft()
        self.dataCnt -= 1
        return

    def AddCandle(self, date, openp, highp, lowp, closep):
        # Add candle data to the structures. Update count.  Pop if we've reached the limit.
        maxval = max(openp, closep)
        minval = min(openp, closep)
        diff = (maxval - minval)/2 + closep
        self.avgd.append(diff)
        self.dates.append(date)
        self.open.append(openp)
        self.high.append(highp)
        self.low.append(lowp)
        self.close.append(closep)
        self.dataCnt += 1

        # Check to see if we need to pop a candle
       # if(self.dataCnt > self.maxSize):
       #     self.PopCandle()

        return

    def InitCandleStats(self, ohlcdata):

        candleLen = []

        for i in range(0, len(ohlcdata)):
            if(ct.IsDoji(ohlcdata['Open'][i], ohlcdata['High'][i], ohlcdata['Low'][i], ohlcdata['Close'][i]) == 0):
                candle = ct.GetCandleBodyLen(ohlcdata['Open'][i], ohlcdata['Close'][i])
                candleLen.append(candle)

        self.candleAvgLen = numpy.mean(candleLen)
        self.candleStdDev = numpy.std(candleLen)

        print candleLen
        print "Total number of candles: ", len(ohlcdata)
        print "Candle len of: %d candles. Avg: %f, StdDev: %f" % (len(candleLen), self.candleAvgLen, self.candleStdDev)

        return


    def IsCandleOutsideStdDev(self, openp, closep):
        candlelen = max(openp, closep) - min(openp, closep)

        if(candlelen >= (self.candleStdDev + self.candleAvgLen)):
            return 1
        else:
            return 0


    def DetectWhipsaw(self):
        whipsawDetected = 0
        stoch = it.GetStochValues(self.high, self.low, self.close, 20, 5, 5)
        slowstoch = stoch[1]
        faststoch = stoch[0]

        # Check to see if current state is whipsaw. If it is then see if we've come across any condition to
        # transition states.
        if(self.state == self.whipsaw):
            whipsawDetected = 1
            if((slowstoch[-1] > 80) or (slowstoch[-1] < 20)):
                self.state = self.unknown
                whipsawDetected = 0

        # Now check to see if we're in middle territory and if we've reversed direction.  If so then a whipsaw has
        # been detected.
        if((faststoch[-1] < 80) and (faststoch[-1] > 20)):
            if((faststoch[-3] > faststoch[-2]) and (faststoch[-1] > faststoch[-2])):
                self.state = self.whipsaw
                whipsawDetected = 1
            elif((faststoch[-3] < faststoch[-2]) and (faststoch[-1] < faststoch[-2])):
                self.state = self.whipsaw
                whipsawDetected = 1

        return whipsawDetected


    def DetectRange(self, slope):
        rangeDetected = 0

        #print slope
        if((slope > -53) and (slope < 53)):
            rangeDetected = 1
            self.state = self.range
        elif(self.state == self.range): # If we're not in range then exit this state?
            self.state = self.unknown

        return rangeDetected


    def DetectBull(self, slope):
        bullDetected = 0

        if((slope > 60)):
            bullDetected = 1
            self.state = self.bullish

        return bullDetected


    def DetectBear(self, slope):
        bearDetected = 0

        if(slope < -60):
            bearDetected = 1
            self.state = self.bearish

        return bearDetected


    def DetectLongTermTrend(self, ):
        longTermTrend = -1
        midTermTrend = -1


        if(len(self.close) > 200):
            stoch50 = it.GetStochValues(self.high, self.low, self.close, 50, 10, 10)
            stoch20 = it.GetStochValues(self.high, self.low, self.close, 20, 5, 5)
            sma50 = it.GetSMAValues(self.close, 50)
            sma200 = it.GetSMAValues(self.close, 200)

            longTermTrend, midTermTrend = ltd.GetTrends(sma50, sma200, stoch50, stoch20, self.midtrend)
            self.midtrend = midTermTrend

        return longTermTrend, midTermTrend


    def UpdateState(self, date, openp, highp, lowp, closep, pointsInRegression=10):
        # Run the algorithm that predicts the current state
        #print openp, highp, lowp, closep
        self.AddCandle(date, openp, highp, lowp, closep)
        #print "avgd len: ", len(self.avgd)

        # Calculate the EMA prepatory to running the nonlinear regression
        smoothed = rt.GetSeriesEMA(self.avgd, self.emaPeriod)
        #print "smoothed len: ", len(smoothed)

        # Run Regression
        points = 5
        mse1, degrees1, slope1 = rt.CalculateNonLinPolyRegression(smoothed, self.mse, points)
        #print date, mse, degrees, points
        points = 10
        mse2, degrees2, slope2 = rt.CalculateNonLinPolyRegression(smoothed, self.mse, points)

        # Get ADX values
        adx = it.GetADXValues2(self.high, self.low, self.close)

        # See if any of last 10 candles are outside of standard deviation
        mycandleoutside = self.IsCandleOutsideStdDev(self.open[-1], self.close[-1])
        candlesOutside = 0
        if(len(self.open) < 11): stopVal = len(self.open)
        else: stopVal = 11
        for i in range(1,stopVal):
            if(self.IsCandleOutsideStdDev(self.open[-i], self.close[-i]) == 1):
                candlesOutside += 1

        # See if a whipsaw state has been detected
        if(self.DetectWhipsaw() == 0):
            if(self.DetectRange(slope1) == 0):
                self.DetectBear(slope1)
                self.DetectBull(slope1)

        # Final detection of trend
        lt, st = self.DetectLongTermTrend()

        #print date, lt, st, len(self.close)
        #print date, self.state, mycandleoutside, candlesOutside, degrees1, degrees2, slope1, slope2, adx[-1], mse1, mse2
        print date, self.open[-1], self.high[-1], self.low[-1], self.close[-1], lt, st
        #print "done with UpdateState"

        # Get the state and return it

        return self.GetState()




