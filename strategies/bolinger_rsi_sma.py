

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

    # Calculate indicators
    data = __RSI ( data, 14 )
    data = __SMA ( data, 13 )
    data = __BB ( data, 20 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if  ( data['SMA_13'][i] > data['BB_middle'][i] ) and ( data["RSI_14"][i] < 50 ) and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif  ( data['SMA_13'][i] < data['BB_middle'][i] ) and ( data["RSI_14"][i] > 50 )  and position == 1:
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



data = __RSI ( data, 14 )
data = __BB ( data, 20 )
data = __SMA ( data, 13 )


if ( ( data['SMA_13'][-1] > data['BB_middle'][-1] ) and ( data['RSI_14'][-1] < 50 ) ):
    print_log ( 'bolinger_rsi_sma.py', 'LONG', [ 'BB', 'RSI', 'SMA_13' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( ( data['SMA_13'][-1] < data['BB_middle'][-1] ) and ( data["RSI_14"][-1] > 50 ) ):
    print_log ( 'bolinger_rsi_sma.py', 'SHORT', [ 'BB', 'RSI', 'SMA_13' ] , backtest_strategy ( ticker , '2020-01-01' ) )

