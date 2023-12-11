#!/usr/bin/env python3
# https://medium.com/codex/algorithmic-trading-with-average-directional-index-in-python-2b5a20ecf06a

import argparse

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

import os, datetime

from math import floor

def __ADX ( data, lookback):
    high = data["High"]
    low = data["Low"]
    close = data["Adj Close"]
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



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    for symbol in args.ticker:

        filename, ext =  os.path.splitext(os.path.basename(__file__))

        csv_file = "{}/data/{}_1d.csv".format( parent_dir, symbol )

        # Get today's date
        today = datetime.datetime.now().date()

        # if the file was downloaded today, read from it
        if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
            data = pd.read_csv ( csv_file, index_col='Date' )
        else:
            # Download data
            data = yf.download ( symbol, start=start_date, progress=False)
            data.to_csv ( csv_file )

        data = __ADX ( data, 14 )

        buy_price, sell_price, adx_signal = implement_adx_strategy ( data['Adj Close'], data['ADX_14_plus_di'], data['ADX_14_minus_di'], data['ADX_14'])

        ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

        ax1.plot ( data['Adj Close'], linewidth=3, color='#ff9800', alpha=0.6)
        ax1.set_title(f'{symbol} CLOSING PRICE')
        ax1.plot ( data.index, buy_price, marker='^', color='#26a69a', markersize=14, linewidth=0, label='BUY SIGNAL')
        ax1.plot ( data.index, sell_price, marker='v', color='#f44336', markersize=14, linewidth=0, label='SELL SIGNAL')

        ax2.plot ( data['ADX_14_plus_di'], color='#26a69a', label='+ DI 14', linewidth=3, alpha=0.3)
        ax2.plot ( data['ADX_14_minus_di'], color='#f44336', label='- DI 14', linewidth=3, alpha=0.3)
        ax2.plot ( data['ADX_14'], color='#2196f3', label='ADX 14', linewidth=3)
        ax2.axhline (25, color='grey', linewidth=2, linestyle='--')
        ax2.legend()
        ax2.set_title(f'{symbol} ADX 14')

        plt.xticks(rotation=45)

        #plt.show()
        filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
        plt.savefig ( filename )

