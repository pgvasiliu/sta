# WilliamsRsi
"""
@author: caitlin
This strategy uses the Williams%R indicator. This momentum indicator oscillates between 0 and -100, and shows
how the current price compares to a 14 day look back period, where a reading near -100 indicates the market is
near the lowest low and a reading near 0 indicates the market is near the highest high. This strategy combines
an 8 period rsi.
"""


def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate indicators
    data = __RSI ( data, 8 )
    data = __WR  ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( ( ( data['WR_14'][i - 2] < -70) | (data['WR_14'][i - 1] < -70) | (data['WR_14'][i] < -70) | (data['WR_14'][i - 3] < -70)) & (( data['RSI_8'][i] < 30) | (data['RSI_8'][i - 1] < 30) | (data['RSI_8'][i - 2] < 30)) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( ( data['WR_14'][i - 2] > -30) | (data['WR_14'][i - 1] > -30) | (data['WR_14'][i] > -30) | (data['WR_14'][i - 3] > -30)) & ((data['RSI_8'][i] > 70) | (data['RSI_8'][i - 1] > 70) | (data['RSI_8'][i - 2] > 70)) ):
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


high = data['High']
low = data['Low']
close = data['Adj Close']

data = __RSI ( data, 8 )
data = __WR ( data, 14 )

# BUY signal: when williams indicator is less than -70 and rsi is less than 30 within the last 3 candles
if ( ( ( data['WR_14'][-3] < -70) | (data['WR_14'][-2] < -70) | (data['WR_14'][-1] < -70) | (data['WR_14'][-4] < -70))
    & (( data['RSI_8'][-1] < 30) | (data['RSI_8'][-2] < 30) | (data['RSI_8'][-3] < 30)) ):
    print_log ( 'williams_rsi.py', 'LONG', [ 'RSI_8', 'WR_14' ] , backtest_strategy ( ticker , '2020-01-01' ))
    plot ( 'williams_rsi.py', ticker, FILE, interval )

# SELL signal: when williams indicator is greater than -30 and rsi is greater than 70 within last 3 candles
if ( ( ( data['WR_14'][-3] > -30) | (data['WR_14'][-2] > -30) | (data['WR_14'][-1] > -30) | (data['WR_14'][-4] > -30))
    & ((data['RSI_8'][-1] > 70) | (data['RSI_8'][-2] > 70) | (data['RSI_8'][-3] > 70)) ):
    print_log ( 'williams_rsi.py', 'SHORT', [ 'RSI_8', 'WR_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( 'williams_rsi.py', ticker, FILE, interval )

