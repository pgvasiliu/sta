
def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __KC ( data, 20, 2 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position ==0 ) and ( data['Adj Close'].iloc[i] < data['KC_lower'].iloc[i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data['Adj Close'].iloc[i] > data['KC_upper'].iloc[i] ):
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

data = __KC (data)

# BUY SIGNAL: candle close is below lower keltner band, stochastic signal is <=30, psar is below the candle
if data['Adj Close'].iloc[-1] < data['KC_lower'].iloc[-1]:
    print_log ( 'kc_close.py', 'LONG', [ 'KC', 'Adj Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL SIGNAL: candle close above upper keltner band, stochastic signal >= 70, psar below candle
if data['Adj Close'].iloc[-1] > data['KC_upper'].iloc[-1]:
    print_log ( 'kc_close.py', 'SHORT', [ 'KC', 'Adj Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

