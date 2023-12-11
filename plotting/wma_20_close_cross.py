#!/usr/bin/env python3

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

def __WSMA( data, n):
    # sma = data.rolling(window=n).mean()
    # ema = data.ewm(span=n, adjust=False).mean()
    weights = np.arange(1, n+1)
    wma = data['Adj Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WMA_{}'.format(n)] = pd.Series(wma)

    return data

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

    # WSMA 20, 50
    data = __WSMA ( data, 20 )

    latest_price = data['Adj Close'][-1]

    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    # Buy/sell signals for  SMA crosses
    data["WMA_20_close_Signal"] = 0.0
    data['WMA_20_close_Signal'] = np.select(
        [ ( data['WMA_20'].shift(1) <  data['Adj Close'].shift(1) ) & ( data['WMA_20'] >  data['Adj Close'] ) ,
          ( data['WMA_20'].shift(1) >  data['Adj Close'].shift(1) ) & ( data['WMA_20'] <  data['Adj Close'] ) ],
    [2, -2])

    # Plot the trading signals
    plt.figure(figsize=(14,7))

    plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol,  )
    plt.plot ( data["WMA_20"], alpha = 0.6, linewidth = 2, color='orange',  label = 'WMA_20',  )

    plt.plot ( data.loc[data["WMA_20_close_Signal"] ==  -2.0].index, data["WMA_20"][data["WMA_20_close_Signal"] ==  -2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
    plt.plot ( data.loc[data["WMA_20_close_Signal"] == 2.0].index, data["WMA_20"][data["WMA_20_close_Signal"] == 2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

    plt.legend(loc = 'upper left')
    plt.title(f'{symbol}_{filename}')

    plt.xticks(rotation=45)
    plt.grid(True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration