#!/usr/bin/env python3

# https://github.com/carlpaulus/Memoire
# https://medium.com/codex/algorithmic-trading-with-williams-r-in-python-5a8e0db9ff1f

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Adj Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    #df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: np.abs(x - x.mean()).mean())

    df['CCI_{}'.format(ndays)] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    return df

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


symbol = 'TSLA'
data = yf.download(symbol, start='2020-01-01', progress=False).drop('Adj Close', axis=1)

data = __CCI ( data, 20 )
data = data.dropna()
data["SMA_15"] = data["Adj Close"].rolling(window=15).mean()

def implement_wr_strategy ( prices, cci, sma ):
    buy_price = []
    sell_price = []
    cci_signal = []
    signal = 0

    cci_upper_level  =  100
    cci_lower_level  =  (-100)

    for i in range ( len (cci) ):
        if cci[i - 1] < cci_lower_level and cci[i] > cci_lower_level and ( prices[i] > sma[i] ) and ( prices[i - 1] < sma[i - 1]):
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                cci_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                cci_signal.append(0)
        elif cci[i - 1] > cci_upper_level and cci[i]< cci_upper_level and ( prices[i] < sma[i] ) and ( prices[i- 1] > sma[i - 1]):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                cci_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                cci_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            cci_signal.append(0)

    return buy_price, sell_price, cci_signal


buy_price, sell_price, cci_signal = implement_wr_strategy ( data['Adj Close'], data['CCI_20'], data['SMA_15'] )

#  plotting the trading signals
ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Adj Close'], linewidth=2, label=symbol)
ax1.plot ( data['SMA_15'], linewidth=2, label='SMA_15')
ax1.plot ( data.index, buy_price, marker='^', markersize=10, linewidth=0, color='green', label='BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker='v', markersize=10, linewidth=0, color='r', label='SELL SIGNAL')
ax1.legend(loc='upper left', fontsize=12)
ax1.set_title(f'{symbol} CCI_20 SMA_15) TRADING SIGNALS')

ax2.plot ( data['CCI_20'], color='orange', linewidth=2)
ax2.text(s='Overbought', x=data.index[30], y=100, fontsize=14)
ax2.text(s='Oversold', x=data.index[30], y=-100, fontsize=14)
ax2.axhline ( 100, linewidth=1.5, linestyle='--', color='red')
ax2.axhline ( -100, linewidth=1.5, linestyle='--', color='green')
ax2.set_title (f'{symbol} CCI_20  SMA_15')

#plt.show()
plt.savefig ('_plots/' + symbol + '_CCI_20_SMA_15.png')

