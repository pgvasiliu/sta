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

# def __WILLR (high, low, close, period):
from util.wr   import __WR


# Calculate Williams %R and add prefix to column names
wr_period = 20
wr_upper_level = -20
wr_lower_level = -80

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
    data = __WR ( data, wr_period )

    wr_today     = data["WR_20"].iloc[-1]
    wr_yesterday = data["WR_20"].iloc[-2]


    if wr_today <= wr_lower_level:
        print(f"Lower oversold level: {wr_today:.2f}")
    elif wr_today >= wr_upper_level:
        print(f"Upper overbought level: {wr_today:.2f}")
    elif wr_yesterday > wr_upper_level and wr_today < wr_upper_level:
        print(f"Upper overbought level breached from above going down today: {wr_today:.2f}")
    elif wr_yesterday < wr_lower_level and wr_today > wr_lower_level:
        print(f"W%R indicator crossed over from below the lower level today: {wr_today:.2f}")

    print ( data.tail (5) )
