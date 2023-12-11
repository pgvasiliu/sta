# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame



def backtest_strategy ( stock, start_date ):
    """
    Function to backtest a strategy
    """

    csv_file = "./data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # EMA 9, TEMA 30
    data = __TEMA ( data, 30 )

    #print ( data.tail(2))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if (   data["Adj Close"][i] > data["TEMA_30"][i] ) and ( data["Adj Close"][i - 1] < data["TEMA_30"][i - 1] ) and ( data["TEMA_30"][i] > data["TEMA_30"][i - 1] ) and ( position == 0 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["Adj Close"][i] < data["TEMA_30"][i] ) and ( data["Adj Close"][i - 1] > data["TEMA_30"][i - 1] ) and ( data["TEMA_30"][i] < data["TEMA_30"][i - 1] ) and ( position == 1 ):
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
timeframe = '5m'

# TEMA 30
data = __TEMA ( data, 30 )

_close     = data["Adj Close"].iloc[-1]
_close_1   = data["Adj Close"].iloc[-2]

tema_30    = data['TEMA_30'].iloc[-1]
tema_30_1  = data['TEMA_30'].iloc[-2]


if ( _close > tema_30 ) and ( tema_30 > tema_30_1 ) and ( _close > _close_1 ):
    print_log ( 'tema_close.py', 'LONG', [ 'Close', 'TEMA_30' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( _close < tema_30 ) and ( tema_30 < tema_30_1 ) and ( _close < _close_1):
    print_log ( 'tema_close.py', 'SHORT', [ 'Close', 'TEMA_30' ] , backtest_strategy ( ticker , '2020-01-01' ) )

