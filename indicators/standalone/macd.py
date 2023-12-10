#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import numpy as np
import pandas as pd

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the exponential moving averages (EMAs)
    ema_fast = data['Adj Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data['Adj Close'].ewm(span=slow_period, adjust=False).mean()

    # Calculate the MACD line
    macd_line = ema_fast - ema_slow

    # Calculate the signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # Add the MACD and signal lines to the dataframe
    data["MACD"] = macd_line
    data["Signal"] = signal_line

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

    # Calculate the MACD and signal lines using the calculate_macd function
    data = calculate_macd(data)

    ## Find the MACD crossover and crossunder
    #macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
    #macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

    # Get the most recent day and the previous day in the dataframe
    today_data = data.iloc[-1]
    yesterday_data = data.iloc[-2]

    # Check if the MACD line crossed above or below the signal line on the most recent day
    if today_data["MACD"] > today_data["Signal"] and yesterday_data["MACD"] <= yesterday_data["Signal"]:
        print("MACD crossed above signal on", today_data.name)
    elif today_data["MACD"] < today_data["Signal"] and yesterday_data["MACD"] >= yesterday_data["Signal"]:
        print("MACD crossed below signal on", today_data.name)

    # Print the full dataframe with MACD and signal lines
    print(data.tail(5))

