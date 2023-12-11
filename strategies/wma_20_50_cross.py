# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __WSMA (data, 20)
    data = __WSMA (data, 50)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["WSMA_20"][i] > data["WSMA_50"][i] and data["WSMA_20"][i - 1] < data["WSMA_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["WSMA_20"][i] < data["WSMA_50"][i] and data["WSMA_20"][i - 1]  > data["WSMA_50"][i - 1] and position == 1:
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


# Optimal ticker interval for the strategy.
timeframe = '5m'

data = __WSMA ( data, 20 )
data = __WSMA ( data, 50 )


if data["WSMA_20_50_Signal"][-1] == 2:
    print_log ( 'wsma_20_50_cross.py', 'LONG', [ 'WSMA_20', 'WSMA_50', 'WSMA_20_50_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "wsma_20_50_cross.py", ticker, FILE, interval )


if data["SMA_20_50_Signal"][-1] == -2:
    print_log ( 'wsma_20_50_cross.py', 'SHORT', [ 'WSMA_20', 'WSMA_50', 'SMA_20_50_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "wsma_20_50_cross.py", ticker, FILE, interval )
