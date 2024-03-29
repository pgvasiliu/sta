########################
#####  S14: Simple #####
########################


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
    data = __MACD ( data )
    data = __RSI ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( (  data['MACD'][i] > 0)  & ( data['MACD'][i] > data['MACD_SIGNAL'][i] ) & ( data['BB_upper'][i] > data['BB_upper'][i - 1] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["RSI_14"][i-1] > 70 ):
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


data = __BB ( data, 20 )
data = __EMA ( data, 100 )
data = __MACD ( data )
data = __RSI ( data, 14 )

if ( (  data['MACD'][-1] > 0) & ( data['MACD'][-1] > data['MACD_SIGNAL'][-1] ) & ( data['BB_upper'][-1] > data['BB_upper'][-2] )):
    print_log ( 'bolinger_macd.py', 'LONG?', [ 'BB', 'MACD', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_macd.py", ticker, FILE, interval )
    
if ( data['RSI_14'][-1] > 80 ):
    print_log ( 'bolinger_macd.py', 'LONG?', [ 'BB', 'MACD', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_macd.py", ticker, FILE, interval )
