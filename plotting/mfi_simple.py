#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __MFI ( data, window=14):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data['MFI_{}'.format(window)] = mfi

    return data

symbol = 'AAPL'

data = yf.download(symbol,start='2020-01-01', progress=False)
data = __MFI ( data, 14 )


fig = plt.figure(figsize=(14,7))

ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data.index, data['Close'])
ax1.axhline ( y=data['Close'].mean(),color='r')
ax1.axhline ( y=data['Close'].max(),color='b')
ax1.axhline ( y=data['Close'].min(),color='b')

ax1.text ( s='Max Price', x=data['Close'].index[0], y=data['Close'].max(), fontsize=14)
ax1.text ( s='Min Price', x=data['Close'].index[0], y=data['Close'].min(), fontsize=14)
ax1.set_ylabel('Price')
ax1.grid()

ax2 = plt.subplot(2, 1, 2)
# ax2.bar(df.index, df['MFI'], color=df.Positive.map({True: 'g', False: 'r'}))
ax2.bar ( data.index, data['MFI_14'])
ax2.axhline(y=75, color='red')
ax2.axhline(y=30, color='green')
ax2.grid()
ax2.set_ylabel ('Money Flow Index')
ax2.set_xlabel ('Date')
plt.show()

#plt.show()

#plt.savefig ('_plots/' + symbol + '_ROC_simple.png')
