#!/usr/bin/env python3
# https://medium.com/codex/algorithmic-trading-with-average-directional-index-in-python-2b5a20ecf06a

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from math import floor

def __ADX ( data, lookback):
    high = data["High"]
    low = data["Low"]
    close = data["Close"]
    open = data["Open"]

    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()

    data['ADX_{}_plus_di'.format(lookback)] = plus_di
    data['ADX_{}_minus_di'.format(lookback)] = minus_di
    #data['ADX_smooth'.format(lookback)] = adx_smooth
    #data["ADX"] = adx_smooth
    data['ADX_{}'.format(lookback)] = adx_smooth
    return data


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

symbol = 'AAPL'
data = yf.download ('AAPL', start='2020-01-01', progress=False)
data = __ADX ( data, 14 )


ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Close'], linewidth=2, color='#ff9800')
ax1.set_title(f'{symbol} CLOSING PRICE')
ax2.plot ( data['ADX_14_plus_di'], color='#26a69a', label='+ DI 14', linewidth=3, alpha=0.3)
ax2.plot ( data['ADX_14_minus_di'], color='#f44336', label='- DI 14', linewidth=3, alpha=0.3)
ax2.plot ( data['ADX_14'], color='#2196f3', label='ADX 14', linewidth=3)
ax2.axhline(25, color='grey', linewidth=2, linestyle='--')
ax2.legend()
ax2.set_title(f'{symbol} ADX 14')

#plt.show()

plt.savefig ('_plots/' + symbol + '_ADX_simple.png')


