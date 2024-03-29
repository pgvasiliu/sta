# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
#import os
#import numpy as np
#import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# SMA 5, SMA 8
data = __SMA ( data, 13 )
data = __SMA ( data, 34 )

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __SMA (data, 13)
    data = __SMA (data, 34)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["SMA_13"][i] > data["SMA_34"][i] and data["SMA_13"][i - 1] < data["SMA_34"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["SMA_13"][i] < data["SMA_34"][i] and data["SMA_13"][i - 1]  > data["SMA_34"][i - 1] and position == 1:
            position = 0
            sell_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage #+ '%'


if data["SMA_13"][-1] > data["SMA_34"][-1] and data["SMA_13"][-2] < data["SMA_34"][-2]:
    print_log ( 'sma_13_34_cross.py', 'LONG', [ 'SMA_13', 'SMA_34', 'SMA_13_34_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "sma_13_34_cross.py", ticker, FILE, interval )

if data["SMA_13"][-1] < data["SMA_34"][-1] and data["SMA_13"][-2]  > data["SMA_34"][-2]:
    print_log ( 'sma_13_34_cross.py', 'SHORT', [ 'SMA_13', 'SMA_34', 'SMA_13_34_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "sma_13_34_cross.py", ticker, FILE, interval )

