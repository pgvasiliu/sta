#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd

import numpy as np

import os, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()
    #return ao

    # Add the AO to the DataFrame
    data["AO"] = ao

    return data

def implement_ao_crossover ( price, ao ):
    buy_price = []
    sell_price = []
    ao_signal = []
    signal = 0

    # Get today's date
    today = datetime.datetime.now().date()


    for i in range(len(ao)):
        if ao.iloc[i] > 0 and ao.iloc[i-1] < 0:
            if signal != 1:
                buy_price.append(price.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        elif ao.iloc[i] < 0 and ao.iloc[i-1] > 0:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price.iloc[i])
                signal = -1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ao_signal.append(0)
    return buy_price, sell_price, ao_signal

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

    # Calculate indicators
    data = __AO ( data, 5, 34 )
    data = data.dropna()

    buy_price, sell_price, ao_signal = implement_ao_crossover( data['Adj Close'], data['AO'])

    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)

    ax1.plot( data['Adj Close'], label = symbol, color = 'skyblue')
    ax1.plot( data.index, buy_price, marker = '^', markersize = 12, color = '#26a69a', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot( data.index, sell_price, marker = 'v', markersize = 12, color = '#f44336', linewidth = 0, label = 'SELL SIGNAL')
    ax1.legend()
    ax1.set_title(f'{symbol} CLOSING PRICE')


    for i in range(len( data )):
        if data['AO'][i-1] > data['AO'][i]:
            ax2.bar( data.index[i], data['AO'][i], color = '#f44336')
        else:
            ax2.bar ( data.index[i], data['AO'][i], color = '#26a69a')
    ax2.set_title(f'{symbol} AWESOME OSCILLATOR 5,34')

    plt.xticks(rotation=45)

    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration
