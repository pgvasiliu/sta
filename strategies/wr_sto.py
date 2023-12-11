# WilliamsStochastic
'''
This strategy uses the Williams%R Indicator and the stochastic signal line to determine buy and sell signals.
Results are compared for a 5 candle period, using williams indicator values of less than -65 for buy and greater
than -35 for sell, and less than or equal to 35 on the stochastic signal line to buy and greater than or equal to
65 to sell.
@author: Caitlin
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
    data = __STOCHASTIC ( data, 14, 3 )
    data = __WR ( data, 14 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( ( ( data['STO_D'][i] <= 35) | (data['STO_D'][i - 1] <= 35) | ( data['STO_D'][i - 2] <= 35) | (data['STO_D'][i - 3] <= 35) | (data['STO_D'][i - 4] <= 35) | ( data['STO_D'][i - 5] <= 35))
    & (( data['WR_14'][i] < -65) | (data['WR_14'][i - 1] < -65) | ( data['WR_14'][i - 2] < -65) | (data['WR_14'][i - 3] < -65) | (data['WR_14'][i - 4] < -65) | ( data['WR_14'][i - 5] < -65))):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( ( data['STO_D'][i] >= 65) | (data['STO_D'][i - 1] >= 65) | ( data['STO_D'][i -2] >= 65) | (data['STO_D'][i -3] >= 65) | (data['STO_D'][i - 4] >= 65) | ( data['STO_D'][i - 5] >= 65))
    & (( data['WR_14'][i] > -35) | (data['WR_14'][i - 1] > -35) | ( data['WR_14'][i - 2] > -35) | (data['WR_14'][i - 3] > -35) | (data['WR_14'][i - 4] > -35) | ( data['WR_14'][i - 5] > -35))):
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


data = __STOCHASTIC ( data, 14, 3 )
data = __WR ( data, 14 )


# BUY SIGNAL: signal line is less than or equal to 35 and williams indicator is less than -65 within the last 5 candles
if ( ( ( data['STO_D'][-1] <= 35) | (data['STO_D'][-2] <= 35) | ( data['STO_D'][-3] <= 35) | (data['STO_D'][-4] <= 35) | (data['STO_D'][-5] <= 35) | ( data['STO_D'][-6] <= 35))
    & (( data['WR_14'][-1] < -65) | (data['WR_14'][-2] < -65) | ( data['WR_14'][-3] < -65) | (data['WR_14'][-4] < -65) | (data['WR_14'][-5] < -65) | ( data['WR_14'][-6] < -65))):
    print_log ( 'wr_sto.py', 'LONG', [ 'STO', 'WR_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# SELL SIGNAL: signal line is greater than or equal to 65 and williams indicator is greater than -35 within the last 5 candles
if ( ( ( data['STO_D'][-1] >= 65) | (data['STO_D'][-2] >= 65) | ( data['STO_D'][-3] >= 65) | (data['STO_D'][-4] >= 65) | (data['STO_D'][-5] >= 65) | ( data['STO_D'][-6] >= 65))
    & (( data['WR_14'][-1] > -35) | (data['WR_14'][-2] > -35) | ( data['WR_14'][-3] > -35) | (data['WR_14'][-4] > -35) | (data['WR_14'][-5] > -35) | ( data['WR_14'][-6] > -35))):
    print_log ( 'wr_sto.py', 'SHORT', [ 'STO', 'WR_14' ] , backtest_strategy ( ticker , '2020-01-01' ) )

