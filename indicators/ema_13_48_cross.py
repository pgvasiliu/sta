#!/usr/bin/env python3

import argparse

import os,sys,datetime
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __EMA (df, window=9):
from util.ema   import __EMA


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

    # Calculate EMA 9 and EMA 21
    data  = __EMA (data, 13)
    data  = __EMA (data, 48)

    # Check for crossover events
    if data['EMA_13'][-1] > data['EMA_48'][-1] and data['EMA_13'][-2] <= data['EMA_48'][-2]:
        print(f"Crossover event: {symbol} {data.index[-1].date()} EMA_13 crossed over EMA_48")
    elif data['EMA_13'][-1] < data['EMA_48'][-1] and data['EMA_13'][-2] >= data['EMA_48'][-2]:
        print(f"Crossover event: {symbol} {data.index[-1].date()} EMA_13 crossed under EMA_48")

    # Check for signal events
    if data['Adj Close'][-1] > data['Adj Close'][-2] and data['EMA_13'][-1] > data['EMA_48'][-1]:
        print(f"\nSignal event: {symbol} {data.index[-1].date()} Today's close price is above yesterday's and 13 EMA is higher than 48 EMA")

    print ( data.tail (5) )
