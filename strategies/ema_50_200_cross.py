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
data = __EMA  ( data, 50 )
data = __EMA ( data, 200 )

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    csv_file = "./data/{}_1d.csv".format( stock )

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

    # Calculate Stochastic RSI
    data = __EMA (data, 50)
    data = __EMA (data, 200)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["EMA_50"][i] > data["EMA_200"][i] and data["EMA_50"][i - 1] < data["EMA_200"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["EMA_50"][i] < data["EMA_200"][i] and data["EMA_50"][i - 1]  > data["EMA_200"][i - 1] and position == 1:
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


if data["EMA_50"][-1] > data["EMA_200"][-1] and data["EMA_50"][-2] < data["EMA_200"][-2]:
    print_log ( 'ema_50_200_cross.py', 'LONG', [ 'EMA_50', 'EMA_200', 'EMA_50_200_cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if data["EMA_50"][-1] < data["EMA_200"][-1] and data["EMA_50"][-2]  > data["EMA_200"][-2]:
    print_log ( 'ema_50_200_cross.py', 'SHORT', [ 'EMA_50', 'EMA_200', 'EMA_50_200_cross' ], backtest_strategy ( ticker , '2020-01-01' ) )


