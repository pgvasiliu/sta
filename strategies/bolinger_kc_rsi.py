
def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __SMA ( data, 20 )
    data = __BB ( data, 20 )
    data = __KC ( data, 20, 2 )
    data = __RSI ( data, 10 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position ==0 and data["BB_lower"][i] < data["KC_lower"][i] and data["BB_upper"][i] > data["KC_upper"][i] and data["RSI_10"][i] < 30:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and data["BB_lower"][i] < data["KC_lower"][i] and data["BB_upper"][i] > data["KC_upper"][i] and data["RSI_10"][i] > 70:
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

data = __SMA ( data, 20 )
data = __BB ( data, 20 )
data = __KC ( data, 20, 2 )
data = __RSI ( data, 10 )

if ( ( data["BB_lower"][-1] < data["KC_lower"][-1] ) and ( data["BB_upper"][-1] > data["KC_upper"][-1] ) and ( data["RSI_10"][-1] < 30 ) ):
    print_log ( 'bolinger_kc_rsi.py', 'LONG', [ 'BB', 'KC', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_kc_rsi.py", ticker, FILE, interval )

if ( ( data["BB_lower"][-1] < data["KC_lower"][-1] ) and ( data["BB_upper"][-1] > data["KC_upper"][-1] ) and ( data["RSI_10"][-1] > 70 ) ):
    print_log ( 'bolinger_kc_rsi.py', 'SHORT', [ 'BB', 'KC', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "bolinger_kc_rsi.py", ticker, FILE, interval )

