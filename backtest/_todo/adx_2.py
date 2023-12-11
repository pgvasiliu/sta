#!/usr/bin/env python3
# https://medium.com/codex/algorithmic-trading-with-average-directional-index-in-python-2b5a20ecf06a

import argparse
import pandas as pd
import numpy as np
import yfinance as yf
from math import floor

import os, datetime

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



symbol = 'AAPL'
data = yf.download ('AAPL', start='2020-01-01', progress=False)
data = __ADX ( data, 14 )


def implement_adx_strategy(prices, pdi, ndi, adx):
    buy_price = []
    sell_price = []
    adx_signal = []
    signal = 0

    for i in range(len(prices)):
        if adx[i - 1] < 25 and adx[i] > 25 and pdi[i] > ndi[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                adx_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                adx_signal.append(0)
        elif adx[i - 1] < 25 and adx[i] > 25 and ndi[i] > pdi[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                adx_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                adx_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            adx_signal.append(0)

    return buy_price, sell_price, adx_signal


buy_price, sell_price, adx_signal = implement_adx_strategy ( data['Close'], data['ADX_14_plus_di'], data['ADX_14_minus_di'], data['ADX_14'])


position = []
for i in range(len(adx_signal)):
    if adx_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len( data['Close'])):
    if adx_signal[i] == 1:
        position[i] = 1
    elif adx_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i - 1]

close_price = data['Close']
plus_di     = data['ADX_14_plus_di']
minus_di    = data['ADX_14_minus_di']
adx         = data['ADX_14']

adx_signal = pd.DataFrame(adx_signal).rename(columns={0: 'adx_signal'}).set_index ( data.index)
position = pd.DataFrame(position).rename(columns={0: 'adx_position'}).set_index ( data.index)

frames = [close_price, plus_di, minus_di, adx, adx_signal, position]
strategy = pd.concat(frames, join='inner', axis=1)

strategy
strategy[25:30]

aapl_ret = pd.DataFrame(np.diff ( data['Close'])).rename(columns={0: 'returns'})
adx_strategy_ret = []

for i in range(len(aapl_ret)):
    returns = aapl_ret['returns'][i] * strategy['adx_position'][i]
    adx_strategy_ret.append(returns)

adx_strategy_ret_df = pd.DataFrame(adx_strategy_ret).rename(columns={0: 'adx_returns'})
investment_value = 100000
number_of_stocks = floor(investment_value / data['Close'][-1])
adx_investment_ret = []

for i in range(len(adx_strategy_ret_df['adx_returns'])):
    returns = number_of_stocks * adx_strategy_ret_df['adx_returns'][i]
    adx_investment_ret.append(returns)

adx_investment_ret_df = pd.DataFrame(adx_investment_ret).rename(columns={0: 'investment_returns'})
total_investment_ret = round(sum(adx_investment_ret_df['investment_returns']), 2)
profit_percentage = floor((total_investment_ret / investment_value) * 100)
print ('Profit gained from the ADX strategy by investing $100k in {} : {}'.format ( symbol, total_investment_ret))
print ('Profit percentage of the ADX strategy in {} : {}%'.format ( symbol, profit_percentage))
