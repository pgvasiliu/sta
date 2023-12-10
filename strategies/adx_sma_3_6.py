
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
    data = __ADX ( data, 14 )
    data = __SMA ( data, 3 )
    data = __SMA ( data, 6 )

    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( (    data['ADX_14'][i] > 25) & ( ( data["SMA_3"][i]  > data["SMA_6"][i] ) & ( data["SMA_3"][i - 1] < data["SMA_6"][i - 1] ) ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif ( position == 1 ) and ( (    data['ADX_14'][i] < 25 ) & ( ( data["SMA_6"][i]  > data["SMA_3"][i] ) & ( data["SMA_6"][i - 1] < data["SMA_3"][i - 1] ) ) ):
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


data = __ADX ( data, 14 )
data = __SMA ( data, 3 )
data = __SMA ( data, 6 )

if ( (    data['ADX_14'][-1] > 25) & ( ( data["SMA_3"][-1]  > data["SMA_6"][-1] ) & ( data["SMA_3"][-2] < data["SMA_6"][-2] ) ) ):
   print_log ( 'adx_rsy.py', 'LONG', [ 'ADX', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( (    data['ADX_14'][-1] < 25 ) & ( ( data["SMA_6"][-1]  > data["SMA_3"][-1] ) & ( data["SMA_6"][-2] < data["SMA_3"][-2] ) ) ):
    print_log ( 'adx_rsi', 'SHORT', [ 'ADX', 'RSI' ] , backtest_strategy ( ticker , '2020-01-01' ) )

