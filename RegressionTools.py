# RegressionTools.py
# Patrick Neary
# 11/23/2015
#
# Description: Functions for running regressions on data


import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation


def GetCandleEMA(data, emaPeriod):
    # data - candlestick data
    # emaLen = period of EMA (9, 15, etc.)
    # Smooth candlestick data out to help with running it through the regression tools.  This routing takes the midpoint
    # of the open and close price.  It then takes the ema at the specified period and returns that list to the calling
    # function.

    # check to see if there's enough data to calculate the EMA.  If not return 0
    if(len(data) < emaPeriod):
        return []

    # Check size of data.  If it's too large, just take a subset to calculate current EMA.  No need to wast CPU time.
    if(len(data) > emaPeriod*2):
        dataset = data[-(emaPeriod*2):-1]

    else:
        dataset = data

    emadata = pd.ewma(np.array(dataset), span=emaPeriod)
    #print len(emadata)
    #print len(dates)

    return emadata[-1]


def GetSeriesEMA(data, emaPeriod):
    # data - candlestick data
    # emaLen = period of EMA (9, 15, etc.)
    # Smooth candlestick data out to help with running it through the regression tools.  This routing takes the midpoint
    # of the open and close price.  It then takes the ema at the specified period and returns that list to the calling
    # function.

    # check to see if there's enough data to calculate the EMA.  If not return 0
    if(len(data) < emaPeriod):
        return []

    # Check size of data.  If it's too large, just take a subset to calculate current EMA.  No need to wast CPU time.
    #if(len(data) > emaPeriod*2):
    #    dataset = data[-(emaPeriod*2):-1]

    #else:
    #    dataset = data
    dataset = data

    emadata = pd.ewma(np.array(dataset), span=emaPeriod)
    #print len(emadata)
    #print len(dates)

    return emadata




def CalculateNonLinPolyRegression(data, mselimit, pointsInReg=5):
    # initialize to a high value
    minmse = 1000
    mindegrees = 1000

    # Check for valid length in data
    if(len(data) <= pointsInReg):
        return minmse, mindegrees, 0

    # get most recent n points from data to run regression on
    y = data[-(pointsInReg+2):-1]
    #print "Looking at regression of data points: ", len(y)

    # create x values
    X = []
    for i in range(0, len(y)): X.append(float(i)*.005)

    #myreg.NonLinPolyRegression(np.array(x), np.array(emadata), 0.05)
    y = np.array(y)
    X = np.array(X)

    #xmin = min(X)
    #xmax = max(X)
    #ymin = min(y)
    #ymax = max(y)

    degrees = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12, 13, 14, 15]
    #print "Total of %d degrees available" % len(degrees)

    true_fun = lambda X: np.cos(1.5 * np.pi * X)

    # Get slope of linear regression
    clf = LinearRegression()
    clf.fit(X[:, np.newaxis], y)
    slope = clf.coef_

    for i in range(len(degrees)):
        # polynomial regression
        polynomial_features = PolynomialFeatures(degree=degrees[i],
                                             include_bias=False)
        linear_regression = LinearRegression()
        pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])

        pipeline.fit(X[:, np.newaxis], y)

        # Evaluate the models using crossvalidation
        scores = cross_validation.cross_val_score(pipeline,
            X[:, np.newaxis], y, scoring="mean_squared_error", cv=len(X))

        mse = -scores.mean()
        if(mse < minmse):
            minmse = mse
            mindegrees = i+1

        #print(" Degree %d mse %.4f" % (i+1, mse))

        if(mse < mselimit):
            minmse = mse
            mindegrees = i+1
            #print("NonLinPolyRegression reduced to %.4f and has %d degrees" % (mse, mindegrees))
            break

    #print("Finished NonLinPolyRegression with degrees %d" % mindegrees)

    return minmse, mindegrees, slope[0]