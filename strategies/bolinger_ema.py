#############################
##### 25: CLUCMAY72018  #####
#############################
# _freq/user_data/strategies/berlinguyinca/25_ClucMay72018.py

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __BB ( data, 20 )
    data = __EMA ( data, 100 )

    Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20



    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( ( data['Adj Close'][i]   < data['EMA_100'][i] ) & ( data['Adj Close'][i]   < 0.985 * data['BB_lower'][i] ) & ( data['Volume'][i]  < Vol_SMA_30[i] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["Adj Close"][i-1] < data['BB_upper'][i-1] and data["Adj Close"][i] > data['BB_upper'][i] ):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage# + '%'


Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

data = __EMA ( data, 100 )
data = __BB ( data )

if  ( ( data['Adj Close'][i]   < data['EMA_100'][i] ) & (   data['Adj Close'][i]   < 0.985 * data['BB_lower'][i] ) & (   data['Volume'][i]  < Vol_SMA_30[i] ) ):
    print_log ( 'bolinger_ema.py', 'LONG', [ 'BB', 'EMA_100' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_ema.py", ticker, FILE, interval )

#if ( ( data['Adj Close'][-1] > data['BB_middle'][-1] )):
#    print ( f"{ticker} {interval} ---> SHORT ::: 25_CLUCMAY72018 close > BB middle\n" )

