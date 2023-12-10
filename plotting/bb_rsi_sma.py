#!/usr/bin/env python3

import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import yfinance as yf

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Adj Close'].rolling(window=n).mean()
    return data

def __BB (data, window=20):
    std = data['Adj Close'].rolling(window).std()
    data = __SMA ( data, window )
    data['BB_upper']   = data["SMA_20"] + std * 2
    data['BB_lower']   = data["SMA_20"] - std * 2
    data['BB_middle']  = data["SMA_20"]

    return data

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


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'
data = yf.download ( symbol, start='2022-01-01', progress=False)

data = __SMA ( data, 13 )
data = __SMA ( data, 20 )
data = __BB ( data, 20 )
data = __RSI ( data, 14 )


def implement_strategy(prices, sma, middle, rsi ):
    buy_price = []
    sell_price = []
    strategy_signal = []
    signal = 0

    for i in range(len(prices)):
        if ( sma[i] > middle[i] ) and ( rsi[i] < 50 ):
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                strategy_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                strategy_signal.append(0)
        elif  ( sma[i] < middle[i] ) and ( rsi[i] > 50 ):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                strategy_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                strategy_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            strategy_signal.append(0)

    return buy_price, sell_price, strategy_signal

buy_price, sell_price, strategy_signal = implement_strategy( data['Close'], data['SMA_13'], data['BB_middle'], data['RSI_14'])

# TSI PLOT
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

ax1.plot ( data['Adj Close'], linewidth = 2)
ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title(f'{symbol} {filename } TRADING SIGNALS')



ax2.plot ( data['SMA_13'],        linewidth = 2, color = 'orange', label = 'SMA_13')
ax2.plot ( data['Close'], linewidth = 2, color = 'skyblue', label = 'Close')
ax2.set_title(f'{symbol} BB SMA_13 Close')
ax2.legend()

ax2.plot ( data['BB_upper'], label = 'UPPER BB 20', linestyle = '--', linewidth = 1, color = 'black')
ax2.plot ( data['SMA_20'],   label = 'MIDDLE BB 20',linestyle = '--', linewidth = 1.2, color = 'grey')
ax2.plot ( data['BB_lower'], label = 'LOWER BB 20', linestyle = '--', linewidth = 1, color = 'black')

#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

