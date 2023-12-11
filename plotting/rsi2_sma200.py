#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    #data['Trend_{}'.format(n)]= data['Close'] / data['Close'].rolling(n).mean()
    return data

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

data = __RSI ( data, 2)
data = __SMA ( data, 5 )
data = __SMA ( data, 200 )

data = data.dropna()


fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(data['Close'])
ax1.plot(data['SMA_5'], label='SMA_5')
ax1.plot(data['SMA_200'], label='SMA_200')
ax1.set_title('Stock '+ symbol +' Closing Price')
ax1.set_ylabel('Price')
ax1.legend(loc='best')

ax2 = plt.subplot(2, 1, 2)
ax2.plot(data['RSI_2'], label='Relative Strengths Index')

ax2.text(s='Overbought', x=data.RSI_2.index[30], y=70, fontsize=14)
ax2.text(s='Oversold', x=data.RSI_2.index[30], y=30, fontsize=14)

ax2.axhline(y=70, color='red')
ax2.axhline(y=30, color='red')
#ax2.fill_between(data.index, y1=30, y2=70, color='#adccff', alpha='0.3')
ax2.axhline(y=95, color='darkblue')
ax2.axhline(y=5, color='darkblue')
ax2.grid()
ax2.set_ylabel('RSI_2')
ax2.set_xlabel('Date')

#plt.show()
plt.savefig ('_plots/' + symbol + '_RSI2_SMA200.png')
