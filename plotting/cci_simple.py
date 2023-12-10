#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

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

# input
symbol = 'AAPL'


# Read data 
data = yf.download ( symbol,start='2020-01-01', progress=False)
data = __CCI ( data, 20 )

fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data['Adj Close'])
ax1.set_title(symbol +' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot ( data['CCI_20'], label='Commodity Channel Index')
ax2.text(s='Overbought', x=data.index[30], y=100, fontsize=14)
ax2.text(s='Oversold', x=data.index[30], y=-100, fontsize=14)
ax2.axhline(y=100, color='red')
ax2.axhline(y=-100, color='green')
ax2.axhline(y=200, color='darkblue')
ax2.axhline(y=-200, color='darkblue')
ax2.grid()
ax2.set_ylabel('CCI_20')
ax2.set_xlabel('Date')

#plt.show()

plt.savefig ('_plots/' + symbol + '_CCI_simple.png')

