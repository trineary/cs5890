# TickerTools.py
# Patrick Neary
# 11/23/2015
#
# Description:  Tools for working with stock/security data.  Includes acquiring the data and then manipulating it.

from pandas_datareader import data, wb
#from pandas.io.data import web
#from pandas.io.data import Options
#import datetime


def GetSecurityDates(secdata):
    # Input security data returned from yahoo/google.  Grabs the date from the structure, adds it to a list
    # and returns the list.

    dates = secdata.index

    datesList=[]
    for date in dates:
        datesList.append(date.strftime('%Y/%m/%d'))

    return datesList


def GetSecurityData(security, startDate, endDate):
    # This function grabs data from yahoo and is delayed by 15 minutes
    # security - security to read in
    # startDate/endDate in format of startDate = datetime.datetime(2006, 01, 15)

    securityData = data.get_data_yahoo(security, startDate, endDate)

    return securityData



def GetOptionsData(security):
    # This function grabs data from yahoo. delayed by 15 mintues
    # security - security to grab options info for
    # website: http://pandas.pydata.org/pandas-docs/stable/remote_data.html

    #optionData = Options(security, 'yahoo')
    #optdata = optionData.get_all_data()
    optdata = []

    return optdata


def GetCallOptions(security, expiry):
    # This function grabs data from yahoo. delayed by 15 mintues
    # security - security to grab options info for
    # expiry - expiration data of the call expiry = datetime.date(2015, 1, 15)
    # website: http://pandas.pydata.org/pandas-docs/stable/remote_data.html


    #optionData = Options(security, 'yahoo')
    #data = optionData.get_call_data(expiry=expiry)
    # To get only call or put data do the following:
    optdata = []

    return optdata


def GetPutOptions(security, expiry):
    # This function grabs data from yahoo. delayed by 15 mintues
    # security - security to grab options info for
    # expiry - expiration data of the put expiry = datetime.date(2015, 1, 15)
    # website: http://pandas.pydata.org/pandas-docs/stable/remote_data.html

    #optionData = Options(security, 'yahoo')
    #data = optionData.get_put_data(expiry=expiry)
    # To get only call or put data do the following:
    optdata = []

    return optdata


def GetAvailExpiryDates(security):
    # This function grabs data from yahoo. delayed by 15 mintues
    # security - security to grab options info for
    # expiry - expiration data of the put expiry = datetime.date(2015, 1, 15)
    # website: http://pandas.pydata.org/pandas-docs/stable/remote_data.html

    #optionData = Options(security, 'yahoo')
    #data = optionData._expiry_dates
    # To get only call or put data do the following:
    optdata = []

    return optdata

