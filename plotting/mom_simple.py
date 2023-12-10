#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __MOM(data, window=14):
    mom = pd.Series(data['Close'].diff(window), name = 'MOM_' + str(window))

    data['MOM_{}'.format(window)] = mom

    #data = data.join(M)
    return data

symbol = 'AAPL'

data = yf.download(symbol,start='2020-01-01', progress=False)
data = __MOM ( data, 10 )


fig = plt.figure(figsize=(14,7))

ax1 = plt.subplot(2, 1, 1)
ax1.plot ( data['Close'])
ax1.set_title(symbol +' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.plot ( data['MOM_10'], label='MoM', color='green')
ax2.grid()
ax2.set_ylabel('Momemntum')
ax2.set_xlabel('Date')
ax2.legend(loc='best')

#plt.show()

plt.savefig ('_plots/' + symbol + '_MOM_simple.png')
