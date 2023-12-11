

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
    data = __EMA (data, 12)
    data = __RSI ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( ( data["EMA_6"][i] > data["EMA_12"][i] ) and ( data["EMA_6"][i - 1] < data["EMA_12"][i - 1] ) and ( data["RSI_14"][i] > 50 ) and ( data["RSI_14"][i - 1] < 50) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data["EMA_6"][i] < data["EMA_12"][i] ) and ( data["EMA_6"][i - 1] > data["EMA_12"][i - 1] ) and ( data["RSI_14"][i] < 50 ) and ( data["RSI_14"][i - 1] > 50 ) ):
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


# EMA, RSI
data = __EMA ( data, 6 )
data = __EMA ( data, 12 )
data = __RSI ( data, 14 )

ema6  = data['EMA_6']
ema12 = data['EMA_12']
rsi   = data['RSI_14']
close = data['Adj Close']

# BUY CRITERIA: when 6EMA crosses below 12EMA and RSI value has crossed above 50
if (ema6.iloc[-1] > ema12.iloc[-1] and ema6.iloc[-2] < ema12.iloc[-2]) and ( rsi.iloc[-1] > 50 and rsi.iloc[-2] < 50):
    print_log ( 'ema_6_12_rsi_14.py', 'LONG', [ 'EMA_6', 'EMA_9', 'EMA_12', 'EMA_21', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: when 6EMA crosses above 12EMA and RSI value has crossed below 50
if (ema6.iloc[-1] < ema12.iloc[-1] and ema6.iloc[-2] > ema12.iloc[-2]) and ( rsi.iloc[-1] < 50 and rsi.iloc[-2] > 50):
    print_log ( 'ema_6_12_rsi_14.py', 'SHORT', [ 'EMA_6', 'EMA_9', 'EMA_12', 'EMA_21', 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )



