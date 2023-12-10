

def backtest_strategy(stock, start_date):
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
    data = __EMA ( data, 144 )
    data = __EMA ( data, 169 )
    data = __SMA ( data, 5   )
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0) and ( data["Adj Close"][i] > data["SMA_5"][i] and data["EMA_144"][i] > data["EMA_169"][i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif ( position == 1 ) and ( data["Adj Close"][i] < data["SMA_5"][i] and data["EMA_144"][i] < data["EMA_169"][i] ):
            position = 0
            sell_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


data = __SMA ( data, 5 )
data = __EMA ( data, 144 )
data = __EMA ( data, 169 )

#data['EMA_144'] = data['Adj Close'].ewm(span=144, min_periods=144, adjust=False).mean()
#data['EMA_169'] = data['Adj Close'].ewm(span=169, min_periods=169, adjust=False).mean()
#data['SMA_5'] = data['Adj Close'].rolling(window=5).mean()


close   = data['Adj Close']
ema_144 = data['EMA_144']
ema_169 = data['EMA_169']
sma_5   = data['SMA_5']

# BUY CRITERIA: closing price is above SMA and 144-period EMA is above 169-period EMA
if (close.iloc[-1] > sma_5.iloc[-1]) and (ema_144.iloc[-1] > ema_169.iloc[-1] ):
    print_log ( 'ema_144_169_sma_5.py', 'LONG_TREND', [ 'EMA_144', 'EMA_169', 'SMA_5' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: if closing price is below SMA and 169-period EMA is above 144-period EMA
if (close.iloc[-1] < sma_5.iloc[-1]) and (ema_169.iloc[-1] > ema_144.iloc[-1] ):
    print_log ( 'ema_144_169_sma_5.py', 'SHORT_TREND', [ 'EMA_144', 'EMA_169', 'SMA_5' ] , backtest_strategy ( ticker , '2020-01-01' ) )

