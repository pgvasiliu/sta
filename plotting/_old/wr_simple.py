#!/usr/bin/env python3

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

    return data

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


symbol = 'AAPL'
data = yf.download ( symbol, start='2020-01-01', progress=False).drop('Adj Close', axis=1)

data = __WR ( data, 20 )
data = data.dropna()

ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)
ax1.plot ( data['Close'], linewidth=2)
ax1.set_title (f'{symbol} CLOSING PRICE')
ax1.set_ylabel('Price')
ax1.legend(loc='best')

ax2.plot ( data['WR_20'], color='orange', linewidth=2)
ax2.axhline ( -20, linewidth=1.5, linestyle='--', color='grey')
ax2.axhline ( -80, linewidth=1.5, linestyle='--', color='grey')
ax2.set_title(f'{symbol} W%R')
ax2.legend(loc='best')
ax2.set_ylabel(f'{symbol} W%R')
ax2.set_xlabel('Date')

#plt.show()
plt.savefig ('_plots/' + symbol + '_WR_simple.png')

