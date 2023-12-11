
def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __KC ( data, 20, 2 )
    data = __ADX ( data, 14 )
    data = __STOCHASTIC ( data, 14, 3 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position ==0 ) and ((data['High'][i] < data['KC_lower'][i] ) & ( data['STO_K'][i] <= 20 ) & ( data['ADX_14'][i] >= 20)):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ((data['Low'][i] > data['KC_upper'][i] ) & ( data['STO_K'][i] >= 80 ) & ( data['ADX_14'][i] >= 20) ):
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

data = __KC ( data )
data = __ADX ( data, 14 )

# BUY SIGNAL: candle close is below lower keltner band, stochastic signal is <=20, psar is below the candle
if ((data['High'][-1] < data['KC_lower'][-1] ) & ( data['STO_K'][-1] <= 20 ) & ( data['ADX_14'][-1] >= 20)):
    print_log ( 'adx_kc_sto.py', 'LONG', [ 'ADX_14', 'KC' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "adx_kc_sto.py", ticker, FILE, interval )


# SELL SIGNAL: candle close above upper keltner band, stochastic signal >= 80, psar below candle
if ((data['Low'][-1] > data['KC_upper'][-1] ) & ( data['STO_K'][-1] >= 80 ) & ( data['ADX_14'][-1] >= 20) ):
    print_log ( 'adx_kc_sto.py', 'SHORT', [ 'ADX_14', 'KC' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "adx_kc_sto.py", ticker, FILE, interval )
