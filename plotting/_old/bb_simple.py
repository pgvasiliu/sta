#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import yfinance as yf

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data

def __BB (data, window=20):
    std = data['Close'].rolling(window).std()
    data = __SMA ( data, window )
    data['BB_upper']   = data["SMA_20"] + std * 2
    data['BB_lower']   = data["SMA_20"] - std * 2
    data['BB_middle']  = data["SMA_20"]

    return data

symbol = 'AAPL'
data = yf.download( symbol, start='2020-01-01', progress=False)
data = __SMA ( data, 20 )
data = __BB ( data, 20 )


data['Close'].plot    ( label = 'Close PRICE', color = 'skyblue')
data['BB_upper'].plot ( label = 'UPPER BB 20', linestyle = '--', linewidth = 1, color = 'black')
data['SMA_20'].plot   ( label = 'MIDDLE BB 20',linestyle = '--', linewidth = 1.2, color = 'grey')
data['BB_lower'].plot ( label = 'LOWER BB 20', linestyle = '--', linewidth = 1, color = 'black')

plt.legend(loc = 'upper left')
plt.title(f'{symbol} BOLLINGER BANDS')

#plt.show()
plt.savefig ('_plots/' + symbol + '_BB_simple.png')

