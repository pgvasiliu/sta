
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
    data = __KC ( data, 20, 2 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position ==0 ) and ( data['Adj Close'].iloc[i] < data['KC_lower'].iloc[i] ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data['Adj Close'].iloc[i] > data['KC_upper'].iloc[i] ):
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

data = __KC (data)

# BUY SIGNAL: candle close is below lower keltner band, stochastic signal is <=30, psar is below the candle
if data['Adj Close'].iloc[-1] < data['KC_lower'].iloc[-1]:
    print_log ( 'kc_close.py', 'LONG', [ 'KC', 'Adj Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL SIGNAL: candle close above upper keltner band, stochastic signal >= 70, psar below candle
if data['Adj Close'].iloc[-1] > data['KC_upper'].iloc[-1]:
    print_log ( 'kc_close.py', 'SHORT', [ 'KC', 'Adj Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

