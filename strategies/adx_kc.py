#KeltnerAdx
'''
@author: Caitlin
This strategy combines Keltner Channels with ADX. Buy signals are given when at least 3 candles
are at or below the low band, and oversold conditions are confirmed by an adx reading of at least 25.
Sell signals are given when at least 3 candles are at or above the high band, and overbought conditions are
confirmed by an adx reading of at least 20.
'''



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

    # Calculate indicators
    data = __KC ( data, 20, 2 )
    data = __ADX ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position ==0 ) and ( ( data['High'][i] <= data['KC_lower'][i] )  & (data['High'][i - 1] <= data['KC_lower'][i - 1] )  & (data['High'][i - 2] <= data['KC_lower'][i - 2] ) & ( data['ADX_14'][i] >= 20) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data['Low'][i] >= data['KC_upper'][i] ) & (data['Low'][i - 1] >= data['KC_upper'][i - 1] )  & (data['Low'][i - 2] >= data['KC_upper'][i - 2] ) & ( data['ADX_14'][i] >= 20) ):
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


data = __KC ( data )
data = __ADX ( data, 14 )

# BUY SIGNAL: adx is >= 25 and at least 3 candles are less than or touch the lower keltner band
if ( ( data['High'][-1] <= data['KC_lower'][-1] )
    & (data['High'][-2] <= data['KC_lower'][-2] )
    & (data['High'][-3] <= data['KC_lower'][-3] ) & ( data['ADX_14'][-1] >= 20) ):
    print_log ( 'adx_kc.py', 'LONG', [ 'ADX_14', 'KC' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL SIGNAL: adx is >=25 and at least 3 candles are greater than or touch the upper keltner band
if ( ( data['Low'][-1] >= data['KC_upper'][-1] )
    & (data['Low'][-2] >= data['KC_upper'][-2] )
    & (data['Low'][-3] >= data['KC_upper'][-3] ) & ( data['ADX_14'][-1] >= 20) ):
    print_log ( 'adx_kc.py', 'SHORT', [ 'ADX_14', 'KC' ] , backtest_strategy ( ticker , '2020-01-01' ) )
