#!/usr/bin/env python3

import argparse

import os,sys,datetime

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

def __ROC (df, n=12, m=6):
    df['ROC']   = ( df["Adj Close"] - df["Adj Close"].shift(n))/df["Adj Close"].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df


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

    # Calculate the KDJ indicator using the function
    data = __ROC (data)

    # Print the data
    print(data.tail(10))

