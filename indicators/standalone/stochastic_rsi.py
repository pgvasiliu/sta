#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):

    delta = data["Adj Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi
    return data

def __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3):
    # RSI
    data = __RSI ( data, period)

    # Stochastic RSI
    stochrsi  = (data['RSI_14'] - data['RSI_14'].rolling(period).min()) / (data['RSI_14'].rolling(period).max() - data['RSI_14'].rolling(period).min())
    data['SRSI_K'] = stochrsi.rolling(SmoothK).mean() * 100
    data['SRSI_D'] = data['SRSI_K'].rolling(SmoothD).mean()
    return data



# Define the overbought and oversold levels
overbought = 80
oversold = 20

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
    print (data.tail (5) )

    #rsi = data['RSI']
    data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

    #stochrsi  = (data['RSI'] - data['RSI'].rolling(period).min()) / (data['RSI'].rolling(period).max() - data['RSI'].rolling(period).min())
    #data['TV_SRSI_k'] = stochrsi.rolling(SmoothK).mean() * 100
    #data['TV_SRSI_d'] = data['TV_SRSI_k'].rolling(smoothD).mean()

    print (data.tail (5) )
