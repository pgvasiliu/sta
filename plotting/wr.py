#!/usr/bin/env python3

# https://github.com/carlpaulus/Memoire
# https://medium.com/codex/algorithmic-trading-with-williams-r-in-python-5a8e0db9ff1f

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

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Adj Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

    return data

def implement_wr_strategy(prices, wr):
    buy_price = []
    sell_price = []
    wr_signal = []
    signal = 0

    for i in range(len(wr)):
        if wr.iloc[i - 1] > -80 and wr.iloc[i] < -80:
            if signal != 1:
                buy_price.append(prices.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        elif wr.iloc[i - 1] < -20 and wr.iloc[i] > -20:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices.iloc[i])
                signal = -1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            wr_signal.append(0)

    return buy_price, sell_price, wr_signal

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

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

    if not os.path.exists(args.csv_file):
        # Get stock data from Yahoo Finance
        data = yf.download(symbol, start='2020-01-01', interval=args.interval, progress=False, threads=True )
        data.to_csv ( '{}'.format ( args.csv_file ) )

    # If the csv file is older than 1440 ( 24h * 60min )        
    today = datetime.datetime.now().date()
    if os.path.exists(args.csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(args.csv_file)) > datetime.timedelta(minutes=1440))(args.csv_file):
        # Get stock data from Yahoo Finance
        data = yf.download(symbol, start='2020-01-01', interval=args.interval, progress=False, threads=True )
        data.to_csv ( '{}'.format ( args.csv_file ) )
    
    data = pd.read_csv ( args.csv_file, index_col='Date' )

    data = __WR ( data, 20 )
    data = data.dropna()
    latest_price = data['Adj Close'].iloc[-1]

    data = data.tail(365)
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)


    buy_price, sell_price, wr_signal = implement_wr_strategy ( data['Adj Close'], data['WR_20'])

    #  plotting the trading signals
    ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

    ax1.plot ( data['Adj Close'], linewidth=2, label=symbol)
    ax1.plot ( data.index, buy_price, marker='^', markersize=10, linewidth=0, color='green', label='BUY SIGNAL')
    ax1.plot ( data.index, sell_price, marker='v', markersize=10, linewidth=0, color='r', label='SELL SIGNAL')
    ax1.legend(loc='upper left', fontsize=12)
    ax1.set_title(f'{symbol} W%R TRADING SIGNALS')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.95, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    ax2.plot ( data['WR_20'], color='orange', linewidth=2)
    ax2.axhline ( -20, linewidth=1.5, linestyle='--', color='grey')
    ax2.axhline ( -80, linewidth=1.5, linestyle='--', color='grey')
    ax2.set_title (f'{symbol} W%R')

    plt.xticks(rotation=45)
    plt.grid(True)

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration
