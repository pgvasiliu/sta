# AwesomeMacd.py
#timeframe = '1h'


def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __AO ( data, 5, 34 )
    data = __MACD ( data )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( data["MACD"][i] > 0 ) and ( data['AO'][i] > 0 ) and ( data['AO'][i - 1] < 0 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["MACD"][i] < 0 ) and ( data['AO'][i] < 0 ) and ( data['AO'][i - 1] > 0 ):
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
data = __AO ( data )

if (  ( data["MACD"][-1] > 0 ) & ( data['AO'][-1]   > 0 ) & ( data['AO'][-2]   < 0 ) ):
    print_log ( 'ao_macd.py', 'LONG', [ 'AO', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if (  ( data["MACD"][-1] < 0 )  & ( data['AO'][-1]   < 0 ) & ( data['AO'][-2]   > 0 ) ):
    print_log ( 'ao_macd.py', 'SHORT', [ 'AO', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )
