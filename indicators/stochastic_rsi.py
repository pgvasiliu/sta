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

# def STOCHASTIC_RSI ( data, period=14, smoothD=3, SmoothK=3)
from util.stochastic_rsi   import __STOCHASTIC_RSI


# Define the overbought and oversold levels
srsi_overbought = 80
srsi_oversold = 20

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

    data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

    # Apply indicator conditions
    if data['SRSI_K'][-1] > srsi_oversold and data['SRSI_K'][-2] < srsi_oversold:
        print(f"Weak BUY :: Stochastic RSI crossed over oversold level from above, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

    if data['SRSI_K'][-1] > srsi_oversold and data['SRSI_K'][-2] < srsi_oversold:
        print(f"STRONG BUY, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

    if data['SRSI_K'][-2] < srsi_overbought and data['SRSI_K'][-1] > srsi_overbought:
        print(f"Weak SELL :: Stochastic RSI crossed over overbought level from below, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

    if data['SRSI_K'][-2] > srsi_overbought and data['SRSI_K'][-1] < srsi_overbought:
        print(f"STRONG SELL, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

    print (data.tail (5) )
