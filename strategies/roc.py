# BBANDRSI.py
# Optimal timeframe for the strategy
timeframe = '1h'

data = __ROC ( data, 12, 6 )


def backtest_strategy ( stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __ROC ( data, 12, 6 )

# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( data["ROC"].iloc[i-1] < -10 and data["ROC"][i] > -10 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["ROC"].iloc[i-1] > 20 and data["ROC"][i] < 20 ):
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



if ( data["ROC"].iloc[i-2] < -10 and data["ROC"][-1] > -10 ):
    print_log ( 'roc.py', 'LONG', [ 'ROC' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "roc.py", ticker, FILE, interval )

if ( data["ROC"].iloc[i-2] > 20 and data["ROC"][-1] < 20 ):
    print_log ( 'roc.py', 'SHORT', [ 'ROC' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "roc.py", ticker, FILE, interval )


