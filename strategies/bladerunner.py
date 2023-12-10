'''
### Author: Wilson ###
Strategy from:
https://www.ig.com/au/trading-strategies/best-forex-trading-strategies-and-tips-190520#Bladerunner
The first candlestick that touches the EMA is called the ‘signal candle’,
The second candle that moves away from the EMA again is the ‘confirmatory candle’.
Traders would place their open orders at this price level to take advantage of the rebounding price.
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
    data = __EMA (data, 20)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( ( data['Low'][i - 1] <= data['EMA_20'][i - 1] and data['EMA_20'][i - 1] <= data['High'][i - 1]) & ( data['Adj Close'][i] > data['Adj Close'][i - 1])):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( data['Low'].iloc[i - 1] <= data['EMA_20'].iloc[i - 1] and data['EMA_20'].iloc[i - 1] <= data['High'].iloc[i - 1]) & (data['Adj Close'].iloc[i] < data['Adj Close'].iloc[i - 1])):
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


data = __EMA ( data, 20 )

# BUY if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Adj Close'].iloc[-1] > data['Adj Close'].iloc[-2])):
    print_log ( 'bladerunner.py', 'LONG', [ 'EMA_20', 'close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Adj Close'].iloc[-1] < data['Adj Close'].iloc[-2])):
    print_log ( 'bladerunner.py', 'SHORT', [ 'EMA_20', 'close' ] , backtest_strategy ( ticker , '2020-01-01' ) )
