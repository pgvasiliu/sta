#!/usr/bin/env python3

import argparse

import os,sys,datetime

import numpy as np
import pandas as pd

import yfinance as yf

def calculate_macd(data):
    # Calculate the MACD line and signal line
    ema12 = data['Adj Close'].ewm(span=12, adjust=False).mean()
    ema26 = data['Adj Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    # Find the MACD crossover and crossunder
    macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
    macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

    return macd, signal, macd_crossover, macd_crossunder

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

    # Calculate the MACD
    macd, signal, macd_crossover, macd_crossunder = calculate_macd(data)

    # Check if the lines intersected above 0
    intersected_above_0 = (macd_crossover & (macd > 0)).any()

    # Check if the lines intersected below 0
    intersected_below_0 = (macd_crossunder & (macd < 0)).any()

    if intersected_above_0:
        print("MACD lines intersected above 0")

    if intersected_below_0:
        print("MACD lines intersected below 0")

