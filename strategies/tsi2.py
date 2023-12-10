#TSI

data = __TSI ( data, 25, 13, 12 )

line = data['TSI']
signal = data['TSI_SIGNAL']


def backtest_strategy (stock, start_date):
    """
    Function to backtest a strategy
    """

    global FILE, interval
    # if the file was downloaded today, read from it
    data = pd.read_csv ( FILE, index_col='Date' )

    # Calculate Stochastic RSI
    data = __TSI ( data, 25, 13, 12 )

    line = data['TSI']
    signal = data['TSI_SIGNAL']


# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and  (  line.iloc[i] < 0 and signal.iloc[i] < 0 and line.iloc[i-1] < 0 and signal.iloc[i-1] < 0) and \
            ((line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1]) or (
              line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1])):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and (line.iloc[i] > 0 and signal.iloc[i] > 0 and line.iloc[i-1] > 0 and signal.iloc[i-1] > 0) and \
            ((line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1]) or (
              line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1])):
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


# BUY CRITERIA 1: if TSI line and signal line is below 0 and tsi crosses signal line
if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (
    line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
    print_log ( 'tsi2', 'LONG', [ 'TSI' ], backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "tsi2.py", ticker, FILE, interval )


# SELL CRITERIA1: if TSI line and signal line has crossed above 0 and TSI line crosses signal
if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (
    line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
    print_log ( 'tsi2', 'SHORT', [ 'TSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )
    plot ( "tsi2.py", ticker, FILE, interval )

