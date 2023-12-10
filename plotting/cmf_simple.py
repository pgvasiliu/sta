#!/usr/bin/env python3

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

import yfinance as yf

def __CMF (df, window=20):
    close = df['Close']
    low = df['Low']
    high = df['High']
    volume = df['Volume']

    mfv = ( (close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= volume
    cmf = mfv.rolling(window).sum() / volume.rolling(window).sum()

    df["CMF"] = cmf

    return df

symbol = 'AAPL'

data = yf.download(symbol,start='2020-01-01', progress=False)
data = __CMF ( data, 20 )


fig = plt.figure(figsize=(14,7))

ax1 = plt.subplot(3, 1, 1)
ax1.plot ( data['Close'])
ax1.set_title (symbol +' Closing Price')
ax1.set_ylabel('Price')
ax1.set_xlabel('Date')
ax1.legend(loc='best')

ax2 = plt.subplot(3, 1, 2)
ax2.plot ( data['CMF'])
ax2.axhline(y=0, color='red')
ax2.grid()
ax2.set_ylabel('Chaikin Money Flow')

ax3 = plt.subplot(3, 1, 3)
data['Positive'] = data['Open'] < data['Close']
colors = data.Positive.map({True: 'g', False: 'r'})
ax3.bar ( data.index, data['Volume'], color=colors, alpha=0.4)
ax3.set_ylabel('Volume')
ax3.grid(True)

#plt.show()
plt.savefig ('_plots/' + symbol + '_CMF_simple.png')


