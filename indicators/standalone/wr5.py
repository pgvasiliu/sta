#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd

def download_data(ticker, period):
    data = yf.download(ticker, period=period)
    return data

def calculate_wr(high, low, close, window=20):
    wr = (high.rolling(window=window).max() - close) / (high.rolling(window=window).max() - low.rolling(window=window).min()) * -100
    return wr

def __WR (high, low, close, t=20):
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

    #wr = calculate_wr(data['High'], data['Low'], data['Adj Close'], window=20)
    wr = __WR(data['High'], data['Low'], data['Adj Close'], t=20)

    data["WR"] = wr
    data["WR_prev"] = data["WR"].shift(1)
    # Reorder columns: WR_prev   WR
    cols = list(data.columns)
    a, b = cols.index('WR'), cols.index('WR_prev')
    cols[b], cols[a] = cols[a], cols[b]
    data = data[cols]

    upper_level = -20
    lower_level = -80

    today_wr = wr.iloc[-1]
    yesterday_wr = wr.iloc[-2]


    if today_wr <= lower_level:
        print(f"Lower oversold level: {today_wr:.2f}")
    elif today_wr >= upper_level:
        print(f"Upper overbought level: {today_wr:.2f}")
    elif yesterday_wr > upper_level and today_wr < upper_level:
        print(f"Upper overbought level breached from above going down today: {today_wr:.2f}")
    elif yesterday_wr < lower_level and today_wr > lower_level:
        print(f"W%R indicator crossed over from below the lower level today: {today_wr:.2f}")

    print ( data.tail (5) )
