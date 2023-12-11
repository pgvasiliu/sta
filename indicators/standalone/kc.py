#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

def __KC(dataframe, period=20, multiplier=2):
    """
    Calculates the Keltner Channels for a given DataFrame.

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the OHLC data of the asset.
    period (int): Period to calculate the Keltner Channels (default: 20).
    multiplier (float): Multiplier for the Average True Range (ATR) (default: 2).

    Returns:
    pd.DataFrame: A new DataFrame containing the Keltner Channels for the given OHLC data.
    """

    atr_lookback = 10

    tr = pd.DataFrame()
    tr['h_l'] = dataframe['High'] - dataframe['Low']
    tr['h_pc'] = abs(dataframe['High'] - dataframe['Adj Close'].shift())
    tr['l_pc'] = abs(dataframe['Low'] - dataframe['Adj Close'].shift())
    tr['tr'] = tr[['h_l', 'h_pc', 'l_pc']].max(axis=1)

    atr = tr['tr'].rolling(atr_lookback).mean()
    #atr = tr['tr'].ewm(alpha = 1/atr_lookback).mean()

    kc_middle = dataframe['Adj Close'].rolling(period).mean()
    kc_upper = kc_middle + multiplier * atr
    kc_lower = kc_middle - multiplier * atr

    dataframe['KC_upper'] = kc_upper
    dataframe['KC_middle'] = kc_middle
    dataframe['KC_lower'] = kc_lower

    return dataframe

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

    # Calculate the Keltner Channels using the function
    data = __KC (data)


    # Loop through each row in the DataFrame and check if the Close price touches the Upper or Lower Keltner Channel
    #for i, row in kc_df.iterrows():
    #    if df['Adj Close'][i] >= row['KC Upper']:
    #        print("Price touched the Upper Keltner Channel on", i.date())
    #    elif df['Adj Close'][i] <= row['KC Lower']:
    #        print("Price touched the Lower Keltner Channel on", i.date())

    # Check yesterday's close price and send a BUY or SELL message if it touches the KC Upper or Lower band
    yesterday_close = data['Adj Close'][-2]
    if data['KC_lower'].iloc[-2] * 1.01 <= yesterday_close < data['KC_lower'].iloc[-1] and data['Adj Close'].iloc[-1] > yesterday_close:
        print("BUY message")
    elif data['KC_upper'].iloc[-2] * 0.99 >= yesterday_close > data['KC_upper'].iloc[-1] and data['Adj Close'].iloc[-1] < yesterday_close:
        print("SELL message")

