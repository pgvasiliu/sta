'''
This strategy combines ema_crossover_rsi_alternative and a modified ema_crossover_macd to determine buy and sell
signals. Ema_crossover_macd was modified such that 9EMA only needs to be below/above 21EMA to fulfill sell/buy
signals respectively rather than a crossover below or above.
'''


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
    data = __EMA (data, 6)
    data = __EMA (data, 9)
    data = __EMA (data, 12)
    data = __EMA (data, 21)
    data = __RSI ( data, 14 )
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
        if ( position == 0 ) and ( ( ( data["EMA_9"][i - 1] > data["EMA_21"][i - 1]) and (
             ( histogram[i] > 0 and histogram[i - 1] < 0 ) or ( histogram[i] < 0 and histogram[i - 1] > 0))) \
             or ( ( data["EMA_6"][i] > data["EMA_12"][i] ) and ( data["RSI_14"][i] > 50 ) ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( ( data["EMA_9"][i - 1] < data["EMA_21"][i - 1]) and (
             ( histogram.iloc[i] < 0 and histogram[i - 1] > 0) or ( histogram[i] > 0 and histogram[i - 1] < 0 ) ) ) \
             or ( ( data["EMA_6"][i] < data["EMA_12"][i] ) and ( data["RSI_14"][i] < 50 ) ) ):
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


for i in [ 6, 9, 12, 21 ]:
    data = __EMA ( data, i )
data = __RSI ( data, 14 )
data = __MACD ( data )

close = data['Adj Close']
ema6  = data['EMA_6']
ema9  = data['EMA_9']
ema12 = data['EMA_12']
ema21 = data['EMA_21']

histogram = data['MACD_HIST']
#rsi = data['RSI_14']

# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if ( ( data["EMA_9"][-2] > data["EMA_21"][-2]) and (
    (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0))) \
    or ( ( data["EMA_6"][-1] > data["EMA_12"][-1]) and ( data["RSI_14"][-1] > 50)):
    print_log ( 'ema_6_9_12_21_macd_rsi_cross.py', 'LONG', [ 'EMA_6', 'EMA_9', 'EMA_12', 'EMA_21', 'RSI_14', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if ( ( data["EMA_9"][-2] < data["EMA_21"][-2]) and (
    (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0))) \
    or ( ( data["EMA_6"][-1] < data["EMA_12"][-1] ) and ( data["RSI_14"][-1] < 50)):
    print_log ( 'ema_6_9_12_21_macd_rsi_cross.py', 'SHORT', [ 'EMA_6', 'EMA_9', 'EMA_12', 'EMA_21', 'RSI_14', 'MACD' ] , backtest_strategy ( ticker , '2020-01-01' ) )
