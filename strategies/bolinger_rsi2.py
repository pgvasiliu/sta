# BBANDRSI.py
# Optimal timeframe for the strategy
timeframe = '1h'

data = __RSI ( data, 14 )
data = __BB ( data )


def backtest_strategy ( stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __BB ( data, 20 )
    data = __RSI ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( ( data["RSI_14"][i] < 30 ) and ( data["Adj Close"][i] < data['BB_lower'][i] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data['Adj Close'][i] >= data['BB_upper'][i] ) and ( data["RSI_14"][i] >= 70 ) ):
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



if ( (  data["RSI_14"][-1] < 30 ) & ( data["Adj Close"][-1]  < data["BB_lower"][-1] ) ):
    print_log ( 'bolinger_rsi2.py', 'LONG', [ 'BB', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_rsi2.py", ticker, FILE, interval )

#SELL if price is above high bollinger band as rsi is greater than 70
if ( ( data['Adj Close'][-1] >= data['BB_upper'][-1] ) & ( data['RSI_14'][-1] >= 70 ) ):
    print_log ( 'bolinger_rsi2.py', 'SHORT', [ 'BB', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_rsi2.py", ticker, FILE, interval )
