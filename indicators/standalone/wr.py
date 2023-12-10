#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd
import numpy as np
import math

def __WR (high, low, close, t):
    highh = high.rolling(t).max()
    lowl = low.rolling(t).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    csv_file = "../../data/{}_1d.csv".format( symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date', parse_dates=True )
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate Williams %R and add prefix to column names
    n = 20

    data['WR'] = __WR ( data['High'], data['Low'], data['Adj Close'], n )
    data["WR_prev"] = data["WR"].shift(1)

    # Reorder columns: WR_prev   WR
    cols = list(data.columns)
    a, b = cols.index('WR'), cols.index('WR_prev')
    cols[b], cols[a] = cols[a], cols[b]
    data = data[cols]

    # Determine overbought and oversold levels
    overbought_level = -20
    oversold_level = -80

    # Determine cross over and cross under levels
    #cross_over = 0
    #cross_under = -100

    # Use pandas' tail() function to get the last row of data
    last_row = data.tail(1)

    # Check if the last entry is oversold, overbought, crossunder or crossover
    if last_row["WR"].values[0] < oversold_level and last_row["WR_prev"].values[0] >= oversold_level:
        print("Last entry is oversold")
    elif last_row["WR"].values[0] > overbought_level and last_row["WR_prev"].values[0] <= overbought_level:
        print("Last entry is overbought")
    #elif last_row["WR"].values[0] > cross_over and last_row["WR_prev"].values[0] <= cross_over:
    #    print("Last entry is cross over")
    #elif last_row["WR"].values[0] < cross_under and last_row["WR_prev"].values[0] >= cross_under:
    #    print("Last entry is cross under")
    else:
        print("Last entry is not oversold or overbought")

    print ( data.tail(5))
