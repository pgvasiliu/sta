'''
@ Vita
https://www.dailyfx.com/forex/education/trading_tips/daily_trading_lesson/2020/01/09/macd-histogram.html

'''

def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __MACD (data)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and  ( (    data["MACD"].iloc[i] < 0 and data['MACD_SIGNAL'].iloc[i] < 0 and data["MACD"].iloc[i - 1] < 0 and data['MACD_SIGNAL'].iloc[i - 1] < 0 and data["MACD"].iloc[i - 2] < 0 and data['MACD_SIGNAL'].iloc[i - 2] < 0) and ( ( data["MACD"].iloc[i - 2] > data['MACD_SIGNAL'].iloc[i - 2] and data["MACD"].iloc[i] < data['MACD_SIGNAL'].iloc[i]) or ( data["MACD"].iloc[i - 2] < data['MACD_SIGNAL'].iloc[i - 2] and data["MACD"].iloc[i] > data['MACD_SIGNAL'].iloc[i]))  ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( (    data["MACD"].iloc[i] > 0 and data['MACD_SIGNAL'].iloc[i] > 0 and data["MACD"].iloc[i - 1] > 0 and data['MACD_SIGNAL'].iloc[i - 1] > 0 and data['MACD'].iloc[i - 2] > 0 and data['MACD_SIGNAL'].iloc[i - 2] > 0) and ( ( data["MACD"].iloc[i - 2] < data['MACD_SIGNAL'].iloc[i - 2] and data["MACD"].iloc[i] > data['MACD_SIGNAL'].iloc[i] ) or ( data["MACD"].iloc[i - 2] > data['MACD_SIGNAL'].iloc[i - 2] and data["MACD"].iloc[i] < data['MACD_SIGNAL'].iloc[i]))  ):
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

data   = __MACD ( data )

# BUY CRITERIA: if MACD line has crossed signal line and are < 0
if (    data["MACD"].iloc[-1] < 0 and data['MACD_SIGNAL'].iloc[-1] < 0 and data["MACD"].iloc[-2] < 0 and data['MACD_SIGNAL'].iloc[-2] < 0 and
        data["MACD"].iloc[-3] < 0 and data['MACD_SIGNAL'].iloc[-3] < 0) and \
    ( ( data["MACD"].iloc[-3] > data['MACD_SIGNAL'].iloc[-3] and data["MACD"].iloc[-1] < data['MACD_SIGNAL'].iloc[-1]) or ( data["MACD"].iloc[-3] < data['MACD_SIGNAL'].iloc[-3] and data["MACD"].iloc[-1] > data['MACD_SIGNAL'].iloc[-1])):
    print_log ( 'macd_cross2.py', 'LONG', [ 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( "macd_cross2.py", ticker, FILE, interval )

# SELL CRITERIA: if MACD line has crossed signal line and are > 0
if (    data["MACD"].iloc[-1] > 0 and data['MACD_SIGNAL'].iloc[-1] > 0 and data["MACD"].iloc[-2] > 0 and data['MACD_SIGNAL'].iloc[-2] > 0 and 
        data['MACD'].iloc[-3] > 0 and data['MACD_SIGNAL'].iloc[-3] > 0) and \
    ( ( data["MACD"].iloc[-3] < data['MACD_SIGNAL'].iloc[-3] and data["MACD"].iloc[-1] > data['MACD_SIGNAL'].iloc[-1] ) or ( data["MACD"].iloc[-3] > data['MACD_SIGNAL'].iloc[-3] and data["MACD"].iloc[-1] < data['MACD_SIGNAL'].iloc[-1])):
    print_log ( 'macd_cross2.py', 'SHORT', [ 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "macd_cross2.py", ticker, FILE, interval )

