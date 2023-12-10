def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __MACD (data)
    data = __WR (data, 20)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position == 0 and ( data["WR_20"][i-1] > -50 and data["WR_20"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and ( data["WR_20"][i-1] < -50 and data["WR_20"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
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


data = __MACD ( data )
data = __WR  ( data, 20 )

if ( data["WR_20"][i-1] > -50 and data["WR_20"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
    print_log ( 'macd_cross_wr_20.py', 'LONG', [ 'MACD', 'WR_20' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "macd_cross_wr_20.py", ticker, FILE, interval )

if ( data["WR_20"][i-1] < -50 and data["WR_20"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
   print_log ( 'macd_cross_wr_20.py', 'SHORT', [ 'MACD', 'WR_20' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "macd_cross_wr_20.py", ticker, FILE, interval )
