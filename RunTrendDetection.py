# RunTrendDetection.py
# Patrick Neary
# 11/23/2015
#
# Description:  CS5890 main code for running trend detection.


from TrendStateTransition import TransitionState
import TickerTools as tt
import IndicatorTools as it
import RegressionTools as rt
import PlottingTools as pt
import datetime

UNKNOWN = 0
BULL = 1
BEAR = 2
RANGE = 3
WHIPSAW = 4

unknown = []
bulltrend = []
beartrend = []
ranging = []
whipsaw = []
combined = []

transition = TransitionState()

def SetPrediction(prediction):

    if(prediction == UNKNOWN): unknown.append(1)
    else: unknown.append(0)

    if(prediction == BULL): bulltrend.append(1)
    else: bulltrend.append(0)

    if(prediction == BEAR): beartrend.append(1)
    else: beartrend.append(0)

    if(prediction == RANGE): ranging.append(1)
    else: ranging.append(0)

    if(prediction == WHIPSAW): whipsaw.append(1)
    else: whipsaw.append(0)

    combined.append(prediction)

    return

def PrintPredictions(dates):
    # For the time being, I'll just print out what the predictions are.  I can visually inspect the results and
    # see how well the algorithm works.  Later I'll move to plotting the results.

    for d, r in zip(dates, combined):
        print d, r

    return

def RunTrendDetection(stock):

    startDate = datetime.date(2005, 8, 7)
    endDate = datetime.date(2014, 02, 10)

    tickerdata = tt.GetSecurityData(stock, startDate, endDate)
    dates = tt.GetSecurityDates(tickerdata)
    #print dates

    # Initialize transition code
    transition.InitCandleStats(tickerdata)


    # Run Trend detection algorithm against every day in acquired data.. run one day at a time
    for day in range(0, len(tickerdata)):
        prediction, value = transition.UpdateState(dates[day], tickerdata['Open'][day], tickerdata['High'][day],
                                                          tickerdata['Low'][day], tickerdata['Close'][day])

        SetPrediction(value)

    #  After algorithm has been run against all of the data, display the results
    dates = tt.GetSecurityDates(tickerdata)

    # For now, once algorithm has been run, print the dates and the prediction.
    #PrintPredictions(dates)

    return


while True:
    stock = raw_input('Stock to plot: ')
    RunTrendDetection(stock)