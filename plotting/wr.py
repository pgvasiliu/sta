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
        if wr[i - 1] > -80 and wr[i] < -80:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        elif wr[i - 1] < -20 and wr[i] > -20:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
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
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:

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

    data = __WR ( data, 20 )
    data = data.dropna()
    latest_price = data['Adj Close'][-1]

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


    filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration


