
def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __PSAR ( data )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( data["PSAR"].iloc[i] < data["Adj Close"].iloc[i] and data["PSAR"].iloc[i - 1] > data["Adj Close"].iloc[i - 1] ): 
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["PSAR"].iloc[i] > data["Adj Close"].iloc[i] and data["PSAR"].iloc[i - 1] < data["Adj Close"].iloc[i - 1] ):
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



data = __PSAR ( data )

#Buy Criteria - current pSAR below close, previous pSAR above close
if data["PSAR"].iloc[-1] < data["Adj Close"].iloc[-1] and data["PSAR"].iloc[-2] > data["Adj Close"].iloc[-2]:
    print_log ( '32_PSAR', 'LONG', [ 'PSAR' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( "psar.py", ticker, FILE, interval )

#Sell Criteria - current pSAR above close, previous pSAR below close
if data["PSAR"].iloc[-1] > data["Adj Close"].iloc[-1] and data["PSAR"].iloc[-2] < data["Adj Close"].iloc[-2]:
    print_log ( '32_PSAR', 'SHORT', [ 'PSAR' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "psar.py", ticker, FILE, interval )
