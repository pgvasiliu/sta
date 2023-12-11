#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()
    data["AO"] = ao

    return data


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

symbol = 'AAPL'

# EXTRACTING STOCK DATA
data = yf.download ( symbol, start='2020-01-01', progress=False)

data = __AO ( data, 5, 34)
data = data.dropna()

ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)
ax1.plot ( data['Close'])
ax1.set_title(f'{symbol} CLOSING PRICE')

for i in range(len(data)):
    if data['AO'][i-1] > data['AO'][i]:
        ax2.bar ( data.index[i], data['AO'][i], color = '#f44336')
    else:
        ax2.bar ( data.index[i], data['AO'][i], color = '#26a69a')
ax2.set_title(f'{symbol} AWESOME OSCILLATOR 5,34')
#plt.show()
plt.savefig ('_plots/' + symbol + '_AO_simple.png')

