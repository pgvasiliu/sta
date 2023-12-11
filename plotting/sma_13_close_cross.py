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
parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
parser.add_argument('-c', '--csv_file', required=True,  type=str, help='csv_file')
parser.add_argument('-i', '--interval', required=True,  type=str, help='interval')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:

    filename, ext =  os.path.splitext(os.path.basename(__file__))

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

    # SMA
    data["SMA_13"] = data["Adj Close"].rolling(window=13).mean()
    data = data.dropna()

    latest_price = data['Adj Close'][-1]

    # Buy/sell signals for  SMA crosses
    data["SMA_13_Close_Signal"] = 0.0
    data['SMA_13_Close_Signal'] = np.select(
        [ ( data['SMA_13'].shift(1) <  data['Adj Close'].shift(1) ) & ( data['SMA_13'] >  data['Adj Close'] ) ,
          ( data['SMA_13'].shift(1) >  data['Adj Close'].shift(1) ) & ( data['SMA_13'] <  data['Adj Close'] ) ],
    [-2, 2])


    # Plot the trading signals
    #plt.figure(figsize=(14,7))

    # Chart 1 year
    data = data.tail(365)
    latest_price = data['Adj Close'][-1]

    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol + ' Price'  )
    plt.plot ( data["SMA_13"], alpha = 0.6, linewidth = 2, color='#FF006E', label = 'SMA_13' )

    plt.plot ( data.loc[data["SMA_13_Close_Signal"] ==  2.0].index, data["SMA_13"][data["SMA_13_Close_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
    plt.plot ( data.loc[data["SMA_13_Close_Signal"] == -2.0].index, data["SMA_13"][data["SMA_13_Close_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

    plt.legend(loc = 'upper left')
    plt.title(f'{symbol}_{filename}')

    plt.xticks(rotation=45)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend(loc = 'upper left')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})
    plt.grid(True)

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration