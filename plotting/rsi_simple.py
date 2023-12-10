#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):

    delta = data["Close"].diff()

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


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

symbol = 'AAPL'

# EXTRACTING STOCK DATA
data = yf.download ( symbol, start='2020-01-01', progress=False)

data = __RSI ( data, 14)
data = data.dropna()


fig = plt.figure(figsize=(14,7))

ax1 = plt.subplot(2, 1, 1)
ax1.plot( data['Adj Close'])
ax1.set_title(symbol +' Closing Price')
ax1.set_ylabel('Price')

# RSI plot
ax2 = plt.subplot(2, 1, 2)
ax2.plot ( data['RSI_14'], color='orange', linewidth=2.5, label='RSI')

ax2.text(s='Overbought', x=data.RSI_14.index[10], y=70, fontsize=12)
ax2.text(s='Oversold', x=data.RSI_14.index[10], y=30, fontsize=12)

ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
ax2.legend(loc='lower right', fontsize=12)
ax2.set_title(f'{symbol} RSI 14')
ax2.set_xlabel('Date')

#plt.show()

plt.savefig ('_plots/' + symbol + '_RSI_14_simple.png')


