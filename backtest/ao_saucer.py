#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd

import numpy as np

import os, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def append_to_log(logfile, line):
    with open(logfile, 'a') as file:
        file.write(line + '\n')

def __EMA ( data, n=9 ):
    #ema = data['Close'].ewm(span = period ,adjust = False).mean()
    #return ( ema )

    data['EMA_{}'.format(n)] = data['Adj Close'].ewm(span = n ,adjust = False).mean()
    return data

def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()

    # Add the AO to the DataFrame
    data["AO"] = ao

    return data


def backtest_strategy(stock, start_date, logfile):
    """
    Function to backtest a strategy
    """

    csv_file = "../data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    #if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate indicators
    data = __AO ( data, 5, 34 )
    data = __EMA ( data, 200 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        ema_dist = data['Adj Close'].iloc[-i] - data['EMA_200'].iloc[i]

        bar_1 = data['AO'].iloc[i - 2]
        bar_2 = data['AO'].iloc[i - 1]
        bar_3 = data['AO'].iloc[i]

        curr_close = data['Adj Close'].iloc[i]
        curr_200ema = data['EMA_200'].iloc[i]

        # Buy signal
        if  ( position == 0 ) and  ( bar_1 > 0 ) and ( bar_2 > 0 ) and ( bar_3 > 0 ) and ( bar_1 > bar_2 ) and ( bar_2 < bar_3 ) and ( curr_close > curr_200ema ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( bar_1 < 0 ) and ( bar_2 < 0 ) and ( bar_3 < 0 ) and ( bar_1 < bar_2 ) and ( bar_2 > bar_3 ) and ( curr_close < curr_200ema ):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.0f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.0f}%")

    tot = ((total_returns - 100000) / 100000) * 100
    tot = (f"{tot:.0f}")
    line = (f"{name:<25}{stock:>6}{tot:>6} %")
    append_to_log ( logfile, line)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
    parser.add_argument('-l', '--logfile',  required=True, type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date, args.logfile )

