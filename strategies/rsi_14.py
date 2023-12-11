# BBANDRSI.py
# Optimal timeframe for the strategy
timeframe = '1h'

data = __RSI ( data, 14 )


def backtest_strategy ( stock, start_date):
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
    data = __RSI ( data, 14 )

# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( ( data["RSI_14"][i] > 30 ) and ( data["RSI_14"][i - 1] < 30 ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data["RSI_14"][i] < 70 ) and ( data["RSI_14"][i - 1] > 70 ) ):
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



if ( (  data["RSI_14"][-1] > 30 ) & ( data["RSI_14"][-2]  < 30 ) ):
    print_log ( 'rsi_14.py', 'LONG', [ 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( (  data["RSI_14"][-1] < 70 ) & ( data["RSI_14"][-2]  > 70 ) ):
    print_log ( 'rsi_14.py', 'SHORT', [ 'RSI_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )


