# EMA, MACD
"""
@author: vita
This strategy uses the crossover between 9EMA and 21EMA with MACD histogram as confirmation to avoid false signals
http://www.forexfunction.com/trading-strategy-of-ema-crossover-with-macd
"""


def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    csv_file = "./data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    #if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate Stochastic RSI
    data = __EMA (data, 9)
    data = __EMA (data, 21)
    data = __MACD ( data )

    histogram = data['MACD_HIST']

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( data["EMA_9"].iloc[i - 1] > data["EMA_21"].iloc[i - 1] and data["EMA_9"].iloc[i - 2] < data["EMA_21"].iloc[i - 2]) and ( (histogram.iloc[i] > 0 and histogram.iloc[i - 1] < 0) or ( histogram.iloc[i] < 0 and histogram.iloc[i - 1] > 0) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["EMA_9"].iloc[i - 1] < data["EMA_21"].iloc[i - 1] and data["EMA_9"].iloc[i - 2] > data["EMA_21"].iloc[i - 2]) and ( ( histogram.iloc[i] < 0 and histogram.iloc[i - 1] > 0) or (histogram.iloc[i] > 0 and histogram.iloc[i - 1] < 0)):
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


data = __EMA ( data, 9 )
data = __EMA ( data, 21 )
data = __MACD ( data )

histogram = data['MACD_HIST']


# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if ( data["EMA_9"].iloc[-2] > data["EMA_21"].iloc[-2] and data["EMA_9"].iloc[-3] < data["EMA_21"].iloc[-3]) and ( (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0)):
    print_log ( 'ema_9_21_macd.py', 'LONG', [ 'EMA_9', 'EMA_21', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if ( data["EMA_9"].iloc[-2] < data["EMA_21"].iloc[-2] and data["EMA_9"].iloc[-3] > data["EMA_21"].iloc[-3]) and ( ( histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0)):
    print_log ( 'ema_9_21_macd.py', 'SHORT', [ 'EMA_9', 'EMA_21', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )

