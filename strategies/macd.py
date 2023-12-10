

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    data = __MACD (data )
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["MACD_HIST"][i] > 0 and data["MACD_HIST"][i - 1] < 0 and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["MACD_HIST"][i] < 0 and data["MACD_HIST"][i - 1]  > 0 and position == 1:
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


data = __MACD ( data )


if ( data["MACD_HIST"].iloc[-1] > 0 and data["MACD_HIST"].iloc[-2] < 0 ):
   print_log ( 'macd.py', 'LONG', [ 'MACD', 'MACD crossover' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( data["MACD_HIST"].iloc[-1] < 0 and data["MACD_HIST"].iloc[-2] > 0 ):
   print_log ( 'macd.py', 'SHORT', [ 'MACD', 'MACD crossunder' ] , backtest_strategy ( ticker , '2020-01-01' ) )
