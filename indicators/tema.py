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

#def __TEMA (df, window=30):
from util.tema   import __TEMA


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

    # Calculate the TEMA
    data = __TEMA (data, 30)

    # Check if price crosses above/below the TEMA
    close_today     = data['Adj Close'].iloc[-1]
    close_yesterday = data['Adj Close'].iloc[-2]

    tema_30_today     = data['TEMA_30'].iloc[-1]
    tema_30_yesterday = data['TEMA_30'].iloc[-2]


    if close_today > tema_30_today and close_yesterday < tema_30_yesterday:
        print(f"TEMA30 :: STRONG BUY :: {symbol} price crossed above the TEMA")

    if close_today < tema_30_today and close_yesterday > tema_30_yesterday  :
        print(f"TEMA30 :: STRONG SELL :: {symbol} price crossed below the TEMA")

    print ( data.tail(3) )

