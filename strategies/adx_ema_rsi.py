###################################
#####  S36: Strategy 005 hlhb #####
###################################

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicator
    data = __RSI ( data, 10 )
    data = __EMA ( data, 5 )
    data = __EMA ( data, 10 )
    data = __ADX ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position == 0 and (  ( ( data["RSI_10"][i]  > 50 ) & ( data["RSI_10"][i - 1] < 50 ) ) & ( ( data["EMA_5"][i]   > data["EMA_10"][i] ) & ( data["EMA_5"][i - 1]  < data["EMA_10"][i - 1] ) ) & ( data['ADX_14'][i]  > 25) & (   data['Volume'][i]  > 0) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and (  ( (  data["RSI_10"][i] < 50 ) & ( data["RSI_10"][i - 1] > 50 ) )  &  ( ( data["EMA_5"][i]  < data["EMA_10"][i] ) & ( data["EMA_5"][i - 1]  > data["EMA_10"][i - 1] ) ) &  (   data['ADX_14'][i] > 25) &  (   data['Volume'][i] > 0) ):
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

data = __RSI ( data, 10 )
data = __EMA ( data, 5 )
data = __EMA ( data, 10 )
data = __ADX ( data, 14 )

if (  ( ( data["RSI_10"][-1]  > 50 ) & ( data["RSI_10"][-2] < 50 ) )
    & ( ( data["EMA_5"][-1]   > data["EMA_10"][-1] ) & ( data["EMA_5"][-2]  < data["EMA_10"][-2] ) )
    & (   data['ADX_14'][-1]  > 25) 
    & (   data['Volume'][-1]  > 0) ):
    print_log ( 'adx_ema_rsi.py', 'LONG', [ 'EMA_5', 'EMA_10', 'ADX_14', 'RSI_10' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "adx_ema_rsi.py", ticker, FILE, interval )

if (  ( (  data["RSI_10"][-1] < 50 ) & ( data["RSI_10"][-2] > 50 ) )
    &  ( ( data["EMA_5"][-1]  < data["EMA_10"][-1] ) & ( data["EMA_5"][-2]  > data["EMA_10"][-2] ) )
    &  (   data['ADX_14'][-1] > 25)
    &  (   data['Volume'][-1] > 0) ):
    print_log ( 'adx_ema_rsi.py', 'SHORT', [ 'EMA_5', 'EMA_10', 'ADX_14', 'RSI_10' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "adx_ema_rsi.py", ticker, FILE, interval )
