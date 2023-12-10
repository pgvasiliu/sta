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
data = __DWMA ( data, 14 )

def backtest_strategy(stock, start_date):
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

    # Calculate Stochastic RSI
    data = __DWMA (data, 14)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( ( data["Adj Close"][i] > data["DWMA_14"][i] ) and ( data["Adj Close"][i - 1] < data["DWMA_14"][i - 1] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif ( position == 1 ) and ( ( data["Adj Close"][i] < data["DWMA_14"][i] ) and ( data["Close"][i - 1] > data["DWMA_14"][i - 1] ) ):
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

    return percentage + '%'


if ( data["Adj Close"][-1] > data["DWMA_14"][-1] ) and ( data["Adj Close"][-2] < data["DWMA_14"][-2] ):
    print_log ( 'dwma_9_21_cross.py', 'LONG', [ 'DWMA_9', 'DWMA_21', 'DWMA_9_21_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( ( data["Adj Close"][-1] < data["DWMA_14"][-1] ) and ( data["Adj Close"][-2] > data["DWMA_14"][-2] ) ):
    print_log ( 'dwma_9_21_cross.py', 'SHORT', [ 'DWMA_9', 'DWMA_21', 'DWMA_9_21_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )


