#!/usr/bin/env python3

import pandas as pd 
import matplotlib.pyplot as plt 
import math
import numpy as np
import yfinance as yf

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    #data['Trend_{}'.format(n)]= data['Close'] / data['Close'].rolling(n).mean()
    return data


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

symbol = 'AAPL'
data = yf.download ( symbol, start="2020-01-01", progress=False)

n = [20, 50]
for i in n:
    data = __SMA ( data, i )


plt.plot ( data['Close'], label = symbol, linewidth = 5, alpha = 0.3)
plt.plot ( data['SMA_20'], label = 'SMA_20')
plt.plot ( data['SMA_50'], label = 'SMA_50')
plt.title (f'{symbol} Simple Moving Averages (20, 50)')
plt.legend (loc = 'upper left')
#plt.show()
plt.savefig ('_plots/' + symbol + '_SMA_20_50_cross_simple.png')

