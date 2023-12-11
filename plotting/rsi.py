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


def implement_rsi_crossover(price, rsi):
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range ( len(rsi) ):
        if rsi[i] > 30 and rsi[i-1] < 30:
            if signal != 1:
                buy_price.append(price[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi[i] < 70 and rsi[i-1] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)
    return buy_price, sell_price, rsi_signal

buy_price, sell_price, rsi_signal = implement_rsi_crossover( data['Close'], data['RSI_14'])

ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)

ax1.plot( data['Close'], label = symbol, color = 'skyblue')
ax1.plot( data.index, buy_price, marker = '^', markersize = 12, color = '#26a69a', linewidth = 0, label = 'BUY SIGNAL')
ax1.plot( data.index, sell_price, marker = 'v', markersize = 12, color = '#f44336', linewidth = 0, label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title(f'{symbol} CLOSING PRICE')
ax1.set_ylabel('Price')

# RSI plot
ax2.plot ( data['RSI_14'], color='orange', linewidth=2.5, label='RSI')

ax2.text(s='Overbought', x=data.RSI_14.index[10], y=70, fontsize=12)
ax2.text(s='Oversold', x=data.RSI_14.index[10], y=30, fontsize=12)

ax2.axhline(30, linestyle='--', linewidth=1.5, color='grey')
ax2.axhline(70, linestyle='--', linewidth=1.5, color='grey')
ax2.legend(loc='lower right', fontsize=12)
ax2.set_title(f'{symbol} RSI 14')
ax2.set_xlabel('Date')

#plt.show()

plt.savefig ('_plots/' + symbol + '_RSI_14.png')


