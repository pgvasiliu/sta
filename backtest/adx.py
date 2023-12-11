#!/usr/bin/env python3
# RETURN 53%

import yfinance as yf
import pandas as pd
import argparse
import numpy as np

import os, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def append_to_log(logfile, line):
    with open(logfile, 'a') as file:
        file.write(line + '\n')

def __ADX ( data, lookback):
    high = data["High"]
    low = data["Low"]
    close = data["Adj Close"]
    open = data["Open"]

    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()

    data['ADX_{}_plus_di'.format(lookback)] = plus_di
    data['ADX_{}_minus_di'.format(lookback)] = minus_di
    #data['ADX_smooth'.format(lookback)] = adx_smooth
    #data["ADX"] = adx_smooth
    data['ADX_{}'.format(lookback)] = adx_smooth
    return data


def backtest_strategy(stock, start_date, logfile ):
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

    # Calculate indicator
    data = __ADX ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if data["ADX_14"][i-1] < 25 and data["ADX_14"][i] > 25 and data["ADX_14_plus_di"][i] > data["ADX_14_minus_di"][i] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["ADX_14"][i-1] > 25 and data["ADX_14"][i] < 25 and data["ADX_14_minus_di"][i] > data["ADX_14_plus_di"][i] and position == 1:
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

