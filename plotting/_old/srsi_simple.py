#!/usr/bin/env python3

import argparse

import os, datetime

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):
    delta = data["Adj Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    return data

def __SRSI ( data, period=14, SmoothD=3, SmoothK=3):
    # RSI
    data = __RSI ( data, period)

    #LL_RSI = data['RSI'].rolling(14).min()
    #HH_RSI = data['RSI'].rolling(14).max()
    #data['SRSI'] = (data['RSI'] - LL_RSI) / (HH_RSI - LL_RSI)

    # Stochastic RSI
    stochrsi  = (data['RSI_14'] - data['RSI_14'].rolling(period).min()) / (data['RSI_14'].rolling(period).max() - data['RSI_14'].rolling(period).min())
    data['SRSI'] = stochrsi
    data['SRSI_K'] = stochrsi.rolling(SmoothK).mean() * 100
    data['SRSI_D'] = data['SRSI_K'].rolling(SmoothD).mean()
    return data

symbol = 'AAPL'

# Read data 
data = yf.download(symbol,start='2020-01-01', progress=False)
data = __RSI ( data, 14 )
data = __SRSI ( data )

data = data.dropna()

fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data['Close'])
ax1.set_title (symbol +' Closing Price')
ax1.set_ylabel ('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot ( data['SRSI'], label='Stoch RSI')
ax2.text (s='Overbought', x=data.RSI_14.index[30], y=0.8, fontsize=14)
ax2.text (s='Oversold', x=data.RSI_14.index[30], y=0.2, fontsize=14)
ax2.axhline (y=0.8, color='red')
ax2.axhline (y=0.2, color='red')
ax2.grid()
ax2.set_ylabel ('SRSI')
ax2.set_xlabel ('Date')

#plt.show()

plt.savefig ('_plots/' + symbol + '_SRSI_simple.png')

