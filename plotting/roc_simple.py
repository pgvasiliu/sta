#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __ROC (df, n=12, m=6):
    df['ROC']   = ( df["Close"] - df["Close"].shift(n))/df["Close"].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df

symbol = 'AAPL'

data = yf.download(symbol,start='2020-01-01', progress=False)
data = __ROC ( data, 12, 6 )


fig = plt.figure(figsize=(14,7))

ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data['Close'])
ax1.set_title(symbol +' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot ( data['ROC'], label='Rate of Change', color='black')
ax2.axhline(y=0, color='blue', linestyle='--')
ax2.axhline(y=10, color='red')
ax2.axhline(y=-10, color='green')
ax2.grid()
ax2.set_ylabel('Rate of Change')
ax2.set_xlabel('Date')
ax2.legend(loc='best')

#plt.show()

plt.savefig ('_plots/' + symbol + '_ROC_simple.png')
