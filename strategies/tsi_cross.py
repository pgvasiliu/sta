#TSI

data = __TSI ( data, 25, 13, 12 )

line = data['TSI']
signal = data['TSI_SIGNAL']

def backtest_strategy (stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __TSI ( data, 25, 13, 12 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( data["TSI"][i-1] < data["TSI_SIGNAL"][i-1] ) and ( data["TSI"][i] > data["TSI_SIGNAL"][i] ) and ( position == 0 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["TSI"][i-1] > data["TSI_SIGNAL"][i-1] ) and ( data["TSI"][i] < data["TSI_SIGNAL"][i] ) and ( position == 1 ):
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


# BUY CRITERIA:
if data["TSI"][-2] < data["TSI_SIGNAL"][-2] and data["TSI"][-1] > data["TSI_SIGNAL"][-1]:
    print_log ( 'tsi_cross.py', 'LONG', [ 'TSI' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "tsi_cross.py", ticker, FILE, interval )


# SELL CRITERIA:
if data["TSI"][-2] > data["TSI_SIGNAL"][-2] and data["TSI"][-1] < data["TSI_SIGNAL"][-1]:
    print_log ( 'tsi_cross.py', 'SHORT', [ 'TSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "tsi_cross.py", ticker, FILE, interval )

