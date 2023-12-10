#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd

def __TEMA(data, n=30):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data['Adj Close'].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    data['TEMA_{}'.format(n)] = tema
    return data


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

    data = __TEMA ( data, 30 )

    # Check if price crosses above/below the TEMA
    today_close = data['Adj Close'].iloc[-1]
    yesterday_close = data['Adj Close'].iloc[-2]

    today_tema = data['TEMA_30'].iloc[-1]
    yesterday_tema = data['TEMA_30'].iloc[-2]


    if yesterday_close < yesterday_tema and today_close > today_tema:
        print(f"{symbol} price crossed above the TEMA")

    if yesterday_close > yesterday_tema and today_close < today_tema:
        print(f"{symbol} price crossed below the TEMA")

