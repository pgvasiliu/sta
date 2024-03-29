# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


def backtest_strategy (stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # EMA 9, TEMA 30
    data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

    #print ( data.tail(2))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( data['SRSI_K'][i-1] < 20 and data['SRSI_K'][i] > 20 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data['SRSI_K'][i-1] > 80 and data['SRSI_K'][i] < 80 ):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage #+ '%'



# Optimal ticker interval for the strategy.
timeframe = '5m'

data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

if ( data['SRSI_K'][-2] < 20 and data['SRSI_K'][-1] > 20 ):
    print_log ( 'srsi_1.py', 'LONG', [ 'SRSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "srsi_1.py", ticker, FILE, interval )


if ( data['SRSI_K'][-2] > 80 and data['SRSI_K'][-1] < 80 ):
    print_log ( 'srsi_1.py', 'SHORT', [ 'SRSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "srsi_1.py", ticker, FILE, interval )

