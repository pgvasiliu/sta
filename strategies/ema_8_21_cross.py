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
data = __EMA ( data, 8 )
data = __EMA ( data, 21 )

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __EMA (data, 8)
    data = __EMA (data, 21)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["EMA_8"][i] > data["EMA_21"][i] and data["EMA_8"][i - 1] < data["EMA_21"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["EMA_8"][i] < data["EMA_21"][i] and data["EMA_8"][i - 1]  > data["EMA_21"][i - 1] and position == 1:
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


if data["EMA_8"][-1] > data["EMA_21"][-1] and data["EMA_8"][-2] < data["EMA_21"][-2]:
    print_log ( 'ema_8_21_cross.py', 'LONG', [ 'EMA_8', 'EMA_21', 'EMA_8_21_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "ema_8_21_cross.py", ticker, FILE, interval )

if data["EMA_8"][-1] < data["EMA_21"][-1] and data["EMA_8"][-2]  > data["EMA_21"][-2]:
    print_log ( 'ema_8_21_cross.py', 'SHORT', [ 'EMA_8', 'EMA_21', 'EMA_8_21_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "ema_8_21_cross.py", ticker, FILE, interval )

