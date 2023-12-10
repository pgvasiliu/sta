data       = __ADX ( data , 14 )

def backtest_strategy ( stock, start_date ):
    """
    Function to backtest a strategy
    """

    #script_dir = os.path.dirname(os.path.abspath(__file__))
    #parent_dir = os.path.dirname(script_dir)
    #filename, ext =  os.path.splitext(os.path.basename(__file__))

    global FILE
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicator
    data = __ADX ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if data["ADX_14"][i-1] < 25 and data["ADX_14"][i] > 25 and data["ADX_14_plus_di"][i] > data["ADX_14_minus_di"][i] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["ADX_14"][i-1] > 25 and data["ADX_14"][i] < 25 and data["ADX_14_minus_di"][i] > data["ADX_14_plus_di"][i] and position == 1:
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


# BUY SIGNAL: adx is above 25 and the positive DI crosses over negative DI indicates a strong uptrend
if data['ADX_14'].iloc[-1] > 25 and data['ADX_14_plus_di'].iloc[-1] > data['ADX_14_minus_di'].iloc[-1] and data['ADX_14_plus_di'].iloc[-2] <= data['ADX_14_minus_di'].iloc[-2]:
    print_log ( 'adx.py', 'LONG', [ 'ADX_14' ] , backtest_strategy ( ticker , '2020-01-01' )  )

# SELL SIGNAL: adx is above 25 and the negative DI crosses over positive DI indicates a strong downtrend
if data['ADX_14'].iloc[-1] > 25 and data['ADX_14_plus_di'].iloc[-1] < data['ADX_14_minus_di'].iloc[-1] and data['ADX_14_plus_di'].iloc[-2] >= data['ADX_14_minus_di'].iloc[-2]:
    print_log ( 'adx.py', 'SHORT', [ 'ADX_14' ], backtest_strategy ( ticker , '2020-01-01' )  )

