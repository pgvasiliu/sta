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
     temp_df['k_fast'] = 100 * (temp_df["Close"] - low_min)/(high_max - low_min)
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

ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Close'], linewidth=3, color='#ff9800', alpha=0.6, label=symbol)
ax1.set_title ( f'{symbol} CLOSING PRICE', fontsize=14)
ax1.legend( loc='center left', fontsize=10)

ax2.plot ( data['%k'], color='#26a69a', label='Fast Stochastic %k', linewidth=3, alpha=0.3)
ax2.plot ( data['%d'], color='#f44336', label='Slow Stochastic %d', linewidth=3, alpha=0.3)
ax2.axhline ( 20, color='grey', linewidth=2, linestyle='--')
ax2.axhline ( 80, color='grey', linewidth=2, linestyle='--')
ax2.text(s='Overbought', x=data.index[30], y=80, fontsize=14)
ax2.text(s='Oversold', x=data.index[30], y=20, fontsize=14)
ax2.legend ( loc='lower right', fontsize=10)
ax2.set_title ( 'Stochastic Oscillator', fontsize=14)

#plt.show()
plt.savefig ('_plots/' + symbol + '_STO_simple.png')


