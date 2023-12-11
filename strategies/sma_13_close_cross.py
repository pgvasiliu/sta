# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---

# SMA 5, SMA 8
data = __SMA  ( data, 13 )


def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicator
    data = __SMA (data, 13)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["Adj Close"][i] > data["SMA_13"][i] and data["Adj Close"][i - 1] < data["SMA_13"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["Adj Close"][i] < data["SMA_13"][i] and data["Adj Close"][i - 1]  > data["SMA_13"][i - 1] and position == 1:
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


# Price crossover SMA 13
if ( ( data["Adj Close"][-1] > data["SMA_13"][-1] ) and ( data["Adj Close"][-2] < data["SMA_13"][-2] ) ):
    print_log ( 'sma_13_close_cross.py', 'LONG', [ 'SMA_13', 'Close', 'cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "sma_13_close_cross.py", ticker, FILE, interval )

# Price crossunder SMA 13
if ( ( data["Adj Close"][-1] < data["SMA_13"][-1] ) and ( data["Adj Close"][-2] > data["SMA_13"][-2] ) ):
    print_log ( 'sma_13_close_cross.py', 'SHORT', [ 'SMA_13', 'Close', 'cross' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "sma_13_close_cross.py", ticker, FILE, interval )

