# AO CROSSOVER https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies 

def backtest_strategy ( stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __AO ( data, 5, 34 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if  ( position == 0 ) and ( ( data['AO'].iloc[i - 3] <= 0 ) and ( data['AO'].iloc[i - 2] >= 0 ) and ( data['AO'].iloc[i - 1] > data['AO'].iloc[i - 2] ) and ( data['AO'].iloc[i] > data['AO'].iloc[i - 1] ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data['AO'].iloc[i - 3]  >= 0 ) and ( data['AO'].iloc[i - 2] <= 0 ) and ( data['AO'].iloc[i - 1] < data['AO'].iloc[i - 2] ) and ( data['AO'].iloc[i] < data['AO'].iloc[i - 1] ) ):
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



data = __AO ( data, 5, 34 )

'''
The Awesome Oscillator Zero Crossover strategy signals buying and selling opportunities when the Awesome Oscillator (AO) crosses to above or below 0.
When the AO crosses above 0, we wait for 3 consecutive increasing values of AO to confirm bullish movement and then buy. 
When the AO crosses below 0, we wait for 3 consecutive decreasing values of AO to confirm bearish movement and then sell.
Author: Cheryl
'''
# BUY CRITERIA: awesome oscillator crosses from below to above the zero line, followed by 3 increasing values
if  data['AO'].iloc[-4] <= 0 and data['AO'].iloc[-3] >= 0 and \
    data['AO'].iloc[-2] > data['AO'].iloc[-3] and \
    data['AO'].iloc[-1] > data['AO'].iloc[-2]:
    print_log ( 'ao_cross2.py', 'LONG', [ 'AO' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "ao_cross2.py", ticker, FILE, interval )


# SELL CRITERIA: awesome oscillator crosses from above to below the zero line, followed by 3 decreasing values
if data['AO'].iloc[-4]  >= 0 and data['AO'].iloc[-3] <= 0 and \
    data['AO'].iloc[-2] < data['AO'].iloc[-3] and \
    data['AO'].iloc[-1] < data['AO'].iloc[-2]:
    print_log ( 'ao_cross2.py', 'SHORT', [ 'AO' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "ao_cross2.py", ticker, FILE, interval )
