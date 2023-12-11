
#############################
#####  26: EMASkipPump  #####
#############################

def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __BB ( data, 20 )
    data = __EMA ( data, 5 )
    data = __EMA ( data, 12 )
    data = __EMA ( data, 21 )

    Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20


    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and (( data['Volume'][i]  < Vol_SMA_30[i] ) & ( data['Adj Close'][i]   < data['EMA_5'][i] ) & ( data['Adj Close'][i]   < data['EMA_12'][i] ) & ( data['Adj Close'][i]  <= data['BB_lower'][i] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and (( data['Adj Close'][i] > data['EMA_5'][i] ) & ( data['Adj Close'][i] > data['EMA_12'][i] ) & ( data['Adj Close'][i] >= data['BB_upper'][i] ) ):
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

data = __EMA ( data, 5 )
data = __EMA ( data, 12 )
data = __EMA ( data, 21 )

Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

if (( data['Volume'][-1]  < Vol_SMA_30[-1] ) &
    ( data['Adj Close'][-1]   < data['EMA_5'][-1] ) &
    ( data['Adj Close'][-1]   < data['EMA_12'][-1] ) &
    #( data['Close'][0]  == data['min'][0]) &
    ( data['Adj Close'][-1]  <= data['BB_lower'][-1] ) ):
    print_log ( 'bolinger_ema_5_12_vol.py', 'LONG', [ 'BB', 'EMA_5', 'EMA_12', 'EMA_21', 'Vol' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( "bolinger_ema_5_12_vol.py", ticker, FILE, interval )

if (( data['Adj Close'][-1] > data['EMA_5'][-1] ) &
    ( data['Adj Close'][-1] > data['EMA_12'][-1] ) &
    #( data['Close'][0] >= data['max'][-1] ) &
    ( data['Adj Close'][-1] >= data['BB_upper'][-1] ) ):
    print_log ( 'bolinger_ema_5_12_vol.py', 'SHORT', [ 'BB', 'EMA_5', 'EMA_12', 'EMA_21', 'Vol' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_ema_5_12_vol.py", ticker, FILE, interval )
