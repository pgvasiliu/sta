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

filename, ext =  os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, help='ticker')
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

    # SMA
    data["SMA_20"] = data["Adj Close"].rolling(window=20).mean()
    data = data.dropna()

    latest_price = data['Adj Close'][-1]

    # Buy/sell signals for  SMA crosses
    data["SMA_20_Close_Signal"] = 0.0
    data['SMA_20_Close_Signal'] = np.select(
        [ ( data['SMA_20'].shift(1) <  data['Adj Close'].shift(1) ) & ( data['SMA_20'] >  data['Adj Close'] ) ,
          ( data['SMA_20'].shift(1) >  data['Adj Close'].shift(1) ) & ( data['SMA_20'] <  data['Adj Close'] ) ],
    [-2, 2])


    # Plot the trading signals
    #plt.figure(figsize=(14,7))

    # Chart 1 year
    data = data.tail(365)
    latest_price = data['Adj Close'][-1]

    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol + ' Price'  )
    plt.plot ( data["SMA_20"], alpha = 0.6, linewidth = 2, color='#FF006E', label = 'SMA_20' )

    plt.plot ( data.loc[data["SMA_20_Close_Signal"] ==  2.0].index, data["SMA_20"][data["SMA_20_Close_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
    plt.plot ( data.loc[data["SMA_20_Close_Signal"] == -2.0].index, data["SMA_20"][data["SMA_20_Close_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

    plt.legend(loc = 'upper left')
    plt.title(f'{symbol}_{filename}')

    plt.xticks(rotation=45)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend(loc = 'upper left')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    plt.xticks(rotation=45)
    plt.grid(True)

    #plt.show()
    filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
    plt.savefig ( filename )

