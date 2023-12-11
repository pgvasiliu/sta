'''
Larry Connors' 2 period RSI strategy uses mean reversion to provide a short-term buy or sell signal.
When the price is above the 200 Moving Average, and 2-period RSI is below 10, this is a buy signal
When the price is below the 200 Moving Average, and 2-period RSI is above 90, this is a sell signal
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

    # Calculate indicators
    data = __RSI ( data, 2 )
    data = __SMA ( data, 5 )
    data = __SMA ( data, 200 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( data['RSI_2'].iloc[i] < 10 and data['Adj Close'].iloc[i] > data['SMA_200'].iloc[i] and data['Adj Close'].iloc[i] < data['SMA_5'].iloc[i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data['RSI_2'].iloc[i] > 90 and data['Adj Close'].iloc[i] < data['SMA_200'].iloc[i] and data['Adj Close'].iloc[i] > data['SMA_5'].iloc[i] ):
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


data = __RSI ( data, 2 )
data = __SMA ( data, 5 )
data = __SMA ( data, 200 )

# Buy when RSI2 between 0 and 10, and price above 200sma but below 5sma
if data['RSI_2'].iloc[-1] < 10 and data['Adj Close'].iloc[-1] > data['SMA_200'].iloc[-1] and data['Adj Close'].iloc[-1] < data['SMA_5'].iloc[-1]:
    print_log ( 'rsi_sma.py', 'LONG', [ 'SMA_5', 'SMA_200', 'RSI_2' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# Sell when RSI2 between 90 and 100, and price below 200sma but above 5sma
if data['RSI_2'].iloc[-1] > 90 and data['Adj Close'].iloc[-1] < data['SMA_200'].iloc[-1] and data['Adj Close'].iloc[-1] > data['SMA_5'].iloc[-1]:
    print_log ( 'rsi_sma.py', 'SHORT', [ 'SMA_5', 'SMA_200', 'RSI_2' ] , backtest_strategy ( ticker , '2020-01-01' ) )


