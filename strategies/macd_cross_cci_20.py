#######################################
#####  S28: MACDStrategy_crossed  #####
#######################################

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __MACD (data)
    data = __CCI (data, 20)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position == 0 and ( data["CCI_20"][i] < 0 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and ( data["CCI_20"][i] > 0 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
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


data = __MACD ( data )
data = __CCI  ( data, 20 )

if ( ( data['MACD_Signal'].iloc[-1] == 2 ) and ( data['CCI_20'][-1] <= -50.0 )):
    print_log ( 'macd_cross_cci_20.py', 'LONG', [ 'CCI', 'MACD', 'MACD crossover' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( "macd_cross_cci_20.py", ticker, FILE, interval )

if ( ( data['MACD_Signal'].iloc[-1] == -2 ) and ( data['CCI_20'][-1] >= 100.0) ):
    print_log ( 'macd_cross_cci_20.py', 'SHORT', [ 'CCI', 'MACD', 'MACD crossunder' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( "macd_cross_cci_20.py", ticker, FILE, interval )

