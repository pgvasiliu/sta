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


################################
#####  External functions  #####
################################
from util.atr        import __ATR
from util.atr_bands  import __ATR_BANDS

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

    data = __ATR_BANDS ( data, 14 )

    print ( data.tail(5))
    # Get the latest price and check if it's within the ATR bands
    latest_price = data.iloc[-1]['Close']

    atr_bands_upper = data['ATR_BANDS_UPPER'][-1]
    atr_bands_lower = data['ATR_BANDS_LOWER'][-1]


    if latest_price > atr_bands_upper:
        print(f"SELL signal for {symbol} at {latest_price}, above the upper ATR band of {atr_bands_upper}")
    elif latest_price < atr_bands_lower:
        print(f"BUY signal for {symbol} at {latest_price}, below the lower ATR band of {atr_bands_lower}")
    elif latest_price > 0.98 * atr_bands_upper:
        print(f"Warning for {symbol}: the price is within 2% of touching the upper ATR band of {atr_bands_upper}")
    elif latest_price < 1.02* atr_bands_lower:
        print(f"Warning for {symbol}: the price is within 2% of touching the lower ATR band of {atr_bands_lower}")
    else:
        print(f"No signal or warning for {symbol} at {latest_price}")

    print (data.tail(5))
