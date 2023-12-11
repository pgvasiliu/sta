
data = __RSI ( data, 14 )
data = __ADX ( data, 14 )

def backtest_strategy (stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicator
    data = __ADX ( data, 14 )
    data = __RSI ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position == 0 and data["ADX_14"][i] > 35 and data["ADX_14_plus_di"][i] < data["ADX_14_minus_di"][i] and data["RSI_14"][i] < 50:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and data["ADX_14"][i] > 35 and data["ADX_14_plus_di"][i] > data["ADX_14_minus_di"][i] and data["RSI_14"][i] > 50:
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



if data["ADX_14"][-1] > 35 and data["ADX_14_plus_di"][-1] < data["ADX_14_minus_di"][-1] and data["RSI_14"][-1] < 50:
   print_log ( 'adx_rsy.py', 'LONG', [ 'ADX', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if data["ADX_14"][-1] > 35 and data["ADX_14_plus_di"][-1] > data["ADX_14_minus_di"][-1] and data["RSI_14"][-1] > 50:
   print_log ( 'adx_rsi', 'SHORT', [ 'ADX', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )

