
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

    # Calculate indicator
    data = __EMA (data, 13)
    data = __SMA (data, 5)

    data['bull_power'] = data['High'] - data['EMA_13']
    data['bear_power'] = data['Low'] - data['EMA_13']

    ema_dist = data['Adj Close'].iloc[-1] - data['EMA_13'].iloc[-1]


    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if position == 0 and data['bear_power'].iloc[i] < 0 and data['bear_power'].iloc[i] > data['bear_power'].iloc[i - 1] and data['bull_power'].iloc[i] > data['bull_power'].iloc[i - 1] and data['EMA_13'].iloc[i] > data['EMA_13'].iloc[i - 1] and data['Adj Close'].iloc[i] > data['SMA_5'].iloc[i]:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif position == 1 and data['bull_power'].iloc[i] > 0 and data['bull_power'].iloc[i] < data['bull_power'].iloc[i - 1] and data['bear_power'].iloc[i] < data['bear_power'].iloc[i - 1] and data['EMA_13'].iloc[i] < data['EMA_13'].iloc[i - 1] and data['Adj Close'].iloc[i] < data['SMA_5'].iloc[i]:
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
data = __EMA ( data, 13 )

data['bull_power'] = data['High'] - data['EMA_13']

data['bear_power'] = data['Low'] - data['EMA_13']

ema_dist = data['Adj Close'].iloc[-1] - data['EMA_13'].iloc[-1]

# BUY CRITERIA: Bear power’s value is negative but increasing, Bull power’s value is increasing and 13 EMA is increasing. AND price is greater than 5 sma
if  data['bear_power'].iloc[-1] < 0 and data['bear_power'].iloc[-1] > data['bear_power'].iloc[-2] and data['bull_power'].iloc[-1] > data['bull_power'].iloc[-2] and data['EMA_13'].iloc[-1] > data['EMA_13'].iloc[-2] and data['Adj Close'].iloc[-1] > data['SMA_5'].iloc[-1]:
    print_log ( 'elder_ray_ema_13_sma_5.py', 'LONG', [ 'SMA_5', 'EMA_13', 'bull_power' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL CRITERIA: Bull power’s value is positive but decreasing,  Bear power’s value is decreasing and 13 EMA is decreasing. AND price is less than 5 sma
if data['bull_power'].iloc[-1] > 0 and data['bull_power'].iloc[-1] < data['bull_power'].iloc[-2] and data['bear_power'].iloc[-1] < data['bear_power'].iloc[-2] and data['EMA_13'].iloc[-1] < data['EMA_13'].iloc[-2] and data['Adj Close'].iloc[-1] < data['SMA_5'].iloc[-1]:
    print_log ( 'elder_ray_ema_13_sma_5.py', 'SHORT', [ 'SMA_5', 'EMA_13', 'bear_power' ] , backtest_strategy ( ticker , '2020-01-01' ) )

