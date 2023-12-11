# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
#import os
#import numpy as np
#import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
#timeframe = '5m'

# SMA 5, SMA 8
data = __EMAV ( data, 20 )
data = __EMAV ( data, 50 )

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __EMAV (data, 20)
    data = __EMAV (data, 50)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["EMAV_20"][i] > data["EMAV_50"][i] and data["EMAV_20"][i - 1] < data["EMAV_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["EMAV_20"][i] < data["EMAV_50"][i] and data["EMAV_20"][i - 1]  > data["EMAV_50"][i - 1] and position == 1:
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


if data["EMAV_20"][-1] > data["EMAV_50"][-1] and data["EMAV_20"][-2] < data["EMAV_50"][-2]:
    print_log ( 'emav_20_50_cross.py', 'LONG', [ 'EMA_20', 'EMA_50', 'EMA_20_50_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "emav_20_50_cross.py", ticker, FILE, interval )


if data["EMAV_20"][-1] < data["EMAV_50"][-1] and data["EMAV_20"][-2]  > data["EMAV_50"][-2]:
    print_log ( 'emav_20_50_cross.py', 'SHORT', [ 'EMA_20', 'EMA_50', 'EMA_20_50_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "emav_20_50_cross.py", ticker, FILE, interval )

