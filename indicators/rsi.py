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

# def __RSI ( df, window=14 )
from util.rsi   import __RSI


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

    # RSI
    data = __RSI ( data, 14)

    # Define the overbought and oversold levels
    rsi_overbought = 70
    rsi_oversold = 30

    #data['RSI_Crossover']  = np.where ( ( ( data['RSI'].shift(1) < oversold ) & ( data['RSI'] > oversold ) ), 1, 0 )
    #data['RSI_Crossunder'] = np.where ( ( ( data['RSI'].shift(1) > overbought ) & ( data['RSI'] < overbought ) ), 1, 0 )

    print (data.tail (5) )

    if data['RSI_Crossover'].iloc[-1] == 1:
        print("RSI :: SELL :: Stock has crossed over")
    elif data['RSI_Crossunder'].iloc[-1] == 1:
        print("RSI :: SELL :: Stock has crossed under")
    else:
        print("No conditions are met")

    rsi = data['RSI_14']

    # Check if the RSI crosses the overbought or oversold levels
    if rsi[-2] < rsi_oversold and rsi[-1] > rsi_oversold:
        print("RSI crossed oversold level from below")
    elif rsi[-2] > rsi_overbought and rsi[-1] < rsi_overbought:
        print("RSI crossed overbought level from above")
    elif rsi[-2] > rsi_oversold and rsi[-1] < rsi_oversold:
        print("RSI crossed oversold level from above")
    elif rsi[-2] < rsi_overbought and rsi[-1] > rsi_overbought:
        print("RSI crossed overbought level from below")
    else:
        print("RSI is within normal range")


