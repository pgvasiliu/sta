#!/usr/bin/env python3

# https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b


import argparse

import os, datetime

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import matplotlib.dates as mdates

import matplotlib.pyplot as plt
from math import floor

def __MACD (data, m=12, n=26, p=9, pc='Adj Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    #data["MACD"] = data.apply(lambda x: (x["EMA_s"]-x["EMA_l"]), axis=1)
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data

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

# creating the strategy
def implement_strategy(prices, data):
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['MACD_HIST'][i] > 0 and data['MACD_HIST'][i - 1] < 0 and data["CCI_20"][i] < 0:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['MACD_HIST'][i] < 0 and data['MACD_HIST'][i - 1] > 0 and data["CCI_20"][i] < 0:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)

    return buy_price, sell_price, macd_signal


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

filename, ext =  os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
parser.add_argument('-c', '--csv_file', required=True,  type=str, help='csv_file')
parser.add_argument('-i', '--interval', required=True,  type=str, help='interval')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:

    data = pd.read_csv ( args.csv_file, index_col='Date' )

    data = __MACD ( data )
    data = __CCI ( data, 20 )

    latest_price = data['Adj Close'][-1]

    data = data.tail(365)
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    buy_price, sell_price, macd_signal = implement_strategy( data['Adj Close'], data)

    ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

    ax1.plot ( data['Adj Close'] )
    ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')

    ax1.legend()
    ax1.axhline ( y=data['Adj Close'].mean(),color='r')
    ax1.grid()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.95, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    ax2.plot ( data['MACD'], color='grey', linewidth=1.5, label='MACD')
    ax2.plot ( data['MACD_SIGNAL'], color='skyblue', linewidth=1.5, label='SIGNAL')


    for i in range(len( data['Adj Close'])):
        if str( data['MACD_HIST'][i])[0] == '-':
            ax2.bar( data.index[i], data['MACD_HIST'][i], color='#ef5350')
        else:
            ax2.bar( data.index[i], data['MACD_HIST'][i], color='#26a69a')

    plt.legend(loc='lower right')

    plt.xticks(rotation=45)
    plt.grid(True)

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration