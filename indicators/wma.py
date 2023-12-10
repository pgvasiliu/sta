#!/usr/bin/env python3

import argparse

import pandas as pd
import yfinance as yf
import os,sys,datetime

def WMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Adj Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Close'], wma], axis=1)
    #df_wma.columns = ['Close', 'WMA']
    #return df_wma
    #df["WMA"] = wma
    df['WMA_{}'.format( window )] = wma
    return df

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

    window = 16

    # Calculate Double WMA with window size of 10
    data = WMA(data, window)

    # Print first 10 rows of updated dataframe
    print ( data.tail(3) )

