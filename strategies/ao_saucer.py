# awesome saucer
'''
The Awesome Oscillator Saucers strategy looks for a bullish or bearish saucer pattern in the Awesome Oscillator, where close price is greater than 200 EMA.
A bullish saucer pattern consists of 3 positive AO bars which form the curve of a saucer (i.e. the middle value is smallest).
A bearish saucer patter consists of 3 negative AO bars which form the curve of an upside down saucer (i.e. the middle value is greatest (least negative)).
Author: Cheryl
'''



def backtest_strategy ( stock, start_date ):
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
    data = __AO ( data, 5, 34 )
    data = __EMA ( data, 200 )


    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        ema_dist = data['Adj Close'].iloc[-i] - data['EMA_200'].iloc[i]

        bar_1 = data['AO'].iloc[i - 2]
        bar_2 = data['AO'].iloc[i - 1]
        bar_3 = data['AO'].iloc[i]

        curr_close = data['Adj Close'].iloc[i]
        curr_200ema = data['EMA_200'].iloc[i]

        # Buy signal
        if  ( position == 0 ) and  ( bar_1 > 0 ) and ( bar_2 > 0 ) and ( bar_3 > 0 ) and ( bar_1 > bar_2 ) and ( bar_2 < bar_3 ) and ( curr_close > curr_200ema ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( bar_1 < 0 ) and ( bar_2 < 0 ) and ( bar_3 < 0 ) and ( bar_1 < bar_2 ) and ( bar_2 > bar_3 ) and ( curr_close < curr_200ema ):
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


data = __EMA ( data, 200 )
ema_dist = data['Adj Close'].iloc[-1] - data['EMA_200'].iloc[-1]

bar_1 = data['AO'].iloc[-3]
bar_2 = data['AO'].iloc[-2]
bar_3 = data['AO'].iloc[-1]

curr_close = data['Adj Close'].iloc[-1]
curr_200ema = data['EMA_200'].iloc[-1]

# BUY CRITERIA: CONSECUTIVELY: all 3 bars positive, 2 decreasing awesome oscillator values followed by an increase, and close is above the 200EMA
if ( bar_1 > 0 ) and ( bar_2 > 0 ) and ( bar_3 > 0 ) and ( bar_1 > bar_2 ) and ( bar_2 < bar_3 ) and ( curr_close > curr_200ema ):
    print_log ( 'ao_saucer.py', 'LONG', [ 'EMA_200', 'AO' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: CONSECUTIVELY: all 3 bars negative, 2 increasing awesome oscillator values followed by a decrease, and close is below the 200EMA
if ( bar_1 < 0 ) and ( bar_2 < 0 ) and ( bar_3 < 0 ) and ( bar_1 < bar_2 ) and ( bar_2 > bar_3 ) and ( curr_close < curr_200ema ):
    print_log ( 'ao_saucer.py', 'SHORT', [ 'EMA_200', 'AO' ] , backtest_strategy ( ticker , '2020-01-01' ) )
