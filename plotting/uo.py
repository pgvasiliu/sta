#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore")

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


def __UO ( data ):
    data['Prior_Close'] = data['Adj Close'].shift()
    data['BP']          = data['Adj Close'] - data[['Low','Prior_Close']].min(axis=1)
    data['TR']          = data[['High','Prior_Close']].max(axis=1) - data[['Low','Prior_Close']].min(axis=1)

    data['Average7']  = data['BP'].rolling(7).sum()/data['TR'].rolling(7).sum()
    data['Average14'] = data['BP'].rolling(14).sum()/data['TR'].rolling(14).sum()
    data['Average28'] = data['BP'].rolling(28).sum()/data['TR'].rolling(28).sum()

    data['UO'] = 100 * (4*data['Average7']+2*data['Average14']+data['Average28'])/(4+2+1)
    data = data.drop(['Prior_Close','BP','TR','Average7','Average14','Average28'],axis=1)

    return data

def implement_strategy ( price, uo ):
    buy_price = []
    sell_price = []
    uo_signal = []
    signal = 0

    # Get today's date
    today = datetime.datetime.now().date()


    for i in range(len(uo)):
        if uo[i -1] < 35 and uo[i] > 35:
            if signal != 1:
                buy_price.append(price[i])
                sell_price.append(np.nan)
                signal = 1
                uo_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                uo_signal.append(0)
        elif uo[i - 1] > 65 and uo[i] < 65:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price[i])
                signal = -1
                uo_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                uo_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            uo_signal.append(0)
    return buy_price, sell_price, uo_signal



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

    data = __UO ( data )

    latest_price = data['Adj Close'].iloc[-1]

    data = data.tail(365)
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    buy_price, sell_price, uo_signal = implement_strategy ( data['Adj Close'], data['UO'])

    #print ( data.tail(3))

    fig = plt.figure(figsize=(14,7))
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot ( data['Adj Close'])
    ax1.set_title ('Stock '+ symbol +' Closing Price')
    ax1.set_ylabel('Price')

    ax1.plot( data.index, buy_price, marker = '^', markersize = 12, color = '#26a69a', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot( data.index, sell_price, marker = 'v', markersize = 12, color = '#f44336', linewidth = 0, label = 'SELL SIGNAL')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.95, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot ( data['UO'], label='Ultimate Oscillator')

    ax2.axhline(y=70, color='red')
    ax2.axhline(y=50, color='black', linestyle='--')
    ax2.axhline(y=30, color='red')

    ax2.grid()
    #ax2.legend(loc='best')
    ax2.set_ylabel('Ultimate Oscillator')
    ax2.set_xlabel('Date')


    plt.xticks(rotation=45)
    plt.grid(True)

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration
