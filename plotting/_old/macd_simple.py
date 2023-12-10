#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __MACD (data, m=12, n=26, p=9, pc='Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    #data["MACD"] = data.apply(lambda x: (x["EMA_s"]-x["EMA_l"]), axis=1)
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data

# input
symbol = 'AAPL'

# Read data 
data = yf.download(symbol,start='2020-01-01', progress=False)
data = data.dropna()
data = __MACD ( data )


# Line Chart
fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data.index, data['Close'])
ax1.axhline ( y=data['Close'].mean(),color='r')
ax1.grid()
ax1v = ax1.twinx()
ax1v.fill_between ( data.index[0:],0, data.Volume[0:], facecolor='#0079a3', alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*data.Volume.max())
ax1.set_title(symbol +' Closing Price')
ax1.set_ylabel('Price')

labels = ['MACD','MACD_SIGNAL']
ax2 = plt.subplot(2, 1, 2)
data['positive'] = data['MACD_HIST'] > 0
ax2.plot(data[['MACD','MACD_SIGNAL']], label=labels)
ax2.bar(data.index, data['MACD_HIST'], color=data.positive.map({True: 'g', False: 'r'}), label='MACD_HIST')
ax2.grid()
ax2.set_ylabel('MACD')
ax2.set_xlabel('Date')
ax2.legend(loc='best')

#plt.show()

plt.savefig ('_plots/' + symbol + '_MACD_simple.png')

