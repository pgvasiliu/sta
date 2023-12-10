##################################################
#####  PANDAS  Weighted Moving Average(WMA)  #####
##################################################
import pandas as pd
import numpy as np

#def wma(src, length):
#    import talib
#    return talib.WMA(src, length)
#
# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
# Reference for code is taken from tradingview


#  WMA and Double WMA
def WMA(df, window, cl='Close'):
    weights = pd.Series(range(1,window+1))
    wma = df[cl].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    df['WMA_{}'.format(window)] = wma
    df['DWMA_{}'.format(window)] = df['WMA_{}'.format(window)].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    return df

