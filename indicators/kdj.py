#!/usr/bin/env python3

import argparse

import os,sys,datetime
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __KDJ (df)
from util.kdj   import __KDJ


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:

    csv_file = "../data/{}_1d.csv".format( symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date', parse_dates=True )
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate the KDJ indicator using the function
    data = __KDJ (data)

    # Check for overbought and oversold conditions
    if data['KDJ_Overbought'].tail(1).values[0] == 1:
        print(f"{symbol} is currently overbought.")
    if data['KDJ_Oversold'].tail(1).values[0] == 1:
        print(f"{symbol} is currently oversold.")

    data['KDJ_LONG_Signal']  = np.where  ( (data['KDJ_K'] > data['KDJ_D']) & (data['KDJ_K'].shift(1) < data['KDJ_D'].shift(1)), 1, 0)
    data['KDJ_SHORT_Signal'] = np.where ( (data['KDJ_K'] < data['KDJ_D']) & (data['KDJ_K'].shift(1) > data['KDJ_D'].shift(1)), 1, 0)

    # Check for buy or sell signal today
    today = data.index[-1]
    if data.loc[today, 'KDJ_LONG_Signal'] == 1:
        print(f"Buy signal detected for {symbol} on {today.date()}")

    if data.loc[today, 'KDJ_SHORT_Signal'] == 1:
        print(f"Sell signal detected for {symbol} on {today.date()}")


    # Print the data
    print(data.tail(10))
