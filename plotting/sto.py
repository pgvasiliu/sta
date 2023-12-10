#!/usr/bin/env python3

# https://github.com/carlpaulus/Memoire
# https://medium.com/codex/combining-bollinger-bands-and-stochastic-oscillator-to-create-a-killer-trading-strategy-in-python-6ea413a59037

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

def __STO (df, k, d):

     temp_df = df.copy()
     low_min = temp_df["Low"].rolling(window=k).min()
     high_max = temp_df["High"].rolling(window=k).max()

     # Fast Stochastic
     temp_df['k_fast'] = 100 * (temp_df["Adj Close"] - low_min)/(high_max - low_min)
     temp_df['d_fast'] = temp_df['k_fast'].rolling(window=d).mean()

     # Slow Stochastic
     temp_df['%k'] = temp_df["d_fast"]
     temp_df['%d'] = temp_df['%k'].rolling(window=d).mean()

     temp_df = temp_df.drop(['k_fast'], axis=1)
     temp_df = temp_df.drop(['d_fast'], axis=1)

     return temp_df


symbol = 'AAPL'
data = yf.download (symbol, start='2020-01-01', progress=False)
data = __STO ( data, 14, 3 )


# Creating the trading strategy
def implement_osc_strategy(prices, k, d):
    buy_price = []
    sell_price = []
    osc_signal = []
    signal = 0

    for i in range(len(prices)):
        #if k[i] < 10 and d[i] < 10:
        if k[i] > d[i] and k[i] < 20 and d[i] < 20:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                osc_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                osc_signal.append(0)
        #elif k[i] > 90 and d[i] > 90:
        elif k[i] < d[i] and k[i] > 80 and d[i] > 80:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                osc_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                osc_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            osc_signal.append(0)

    return buy_price, sell_price, osc_signal


buy_price, sell_price, rsi_signal = implement_osc_strategy ( data['Adj Close'], data['%k'], data['%d'])

ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Adj Close'], linewidth=3, color='#ff9800', alpha=0.6, label=symbol)
ax1.set_title ( f'{symbol} CLOSING PRICE', fontsize=14)
ax1.plot ( data.index, buy_price, marker='^', color='#26a69a', markersize=12, linewidth=0, label='BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker='v', color='#f44336', markersize=12, linewidth=0, label='SELL SIGNAL')
ax1.legend( loc='center left', fontsize=10)

ax2.plot ( data['%k'], color='#26a69a', label='Fast Stochastic %k', linewidth=3, alpha=0.3)
ax2.plot ( data['%d'], color='#f44336', label='Slow Stochastic %d', linewidth=3, alpha=0.3)
ax2.text(s='Overbought', x=data.index[30], y=80, fontsize=14)
ax2.text(s='Oversold', x=data.index[30], y=20, fontsize=14)
ax2.axhline ( 20, color='grey', linewidth=2, linestyle='--')
ax2.axhline ( 80, color='grey', linewidth=2, linestyle='--')
ax2.legend ( loc='lower right', fontsize=10)
ax2.set_title ( 'Stochastic Oscillator', fontsize=14)

#plt.show()
plt.savefig ('_plots/' + symbol + '_STO.png')


