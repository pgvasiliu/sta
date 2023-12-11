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

    # Calculate indicators
    data = __CCI ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( data['CCI_14'][i-1] < -100 ) & ( data['CCI_14'][i] > -100 ) and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["CCI_14"][i-1] > 100 and data["CCI_14"][i] < 100 ) and position == 1:
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


# Optimal ticker interval for the strategy.
timeframe = '15m'

data = __CCI ( data, 14 )

if data['CCI_Signal_14'][-1] == 2:
    print_log ( 'cci_14.py', 'LONG', [ 'CCI_14' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "cci_14.py", ticker, FILE, interval )

if data['CCI_Signal_14'][-1] == -2:
    print_log ( 'cci_14.py', 'SHORT', [ 'CCI_14' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "cci_14.py", ticker, FILE, interval )