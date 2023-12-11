# https://github.com/WaveyTechLtd/Stock_market_trader_EMA_RSI_ATR
"""
17/01/2021
Code which trys to back test strategy in this video ... https://www.youtube.com/watch?v=7NM7bR2mL7U
Required info is 
- 50EMA 
- 14EMA 
- 8EMA
- Stocastic RSI (K=3, D=3, RSI_length=14, Stocastic_length=14, source=close) 
- ATR - length 14, RMA smoothing
- He was using EURUSD market, not individual stocks
- buying stocks forces you to trade n=1 stock minium, rather than always a percentage of your capital?

# For a Long position 
(1) 8EMA > 14EMA > 50EMA, indicates upward trend
(2) Stocastic cross over
(3) Adj Close > all EMAs

Target is 2 x ATR value, stop loss is 3 x ATR value

# For a short position
(1) 8EMA < 14EMA < 50EMA
(2) Stocastic cross over
(3) Close < all EMAs
Target 2 x ATR value, stop loss is 3 x ATR value.

#############
He reported a 76% win rate over 100 trades ... lets find out if I get the same 
The adjusted closing price amends a stock's closing price to reflect that stock's value after accounting for any corporate actions (stock splits, dividends etc)
More accurate reflection of the value of the stock at the historical time
Use this instead of Close price, better for back testing.
"""


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

    data = __RSI ( data, 14 )

    data["ATR"] = __ATR ( data, 14 )

    data = __EMA ( data, 50 )
    data = __EMA ( data, 14 )
    data = __EMA ( data, 8 )
    data = __STOCHASTIC (data, 14, 3)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    data['STO_Signal'] = np.select(
            [ ( data['STO_K'].shift(1) < 20 ) & ( data['STO_K'] > 20 ),
              ( data['STO_K'].shift(1) > 80 ) & ( data['STO_K'] < 80 ) ],
            [2, -2])

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( position == 0 ) and ( ( ( data["EMA_8"][i]   > data["EMA_14"][i] ) & ( data["EMA_8"][i] > data["EMA_50"][i] ) & ( data["EMA_14"][i] > data["EMA_50"][i] ) ) & ( data['Adj Close'][i] > data['EMA_8'][i] ) & ( data['STO_Signal'].iloc[i] == 2 ) ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( ( ( data['EMA_8'][i] < data['EMA_14'][i] ) and ( data['EMA_8'][i] < data['EMA_50'][i] ) and ( data['EMA_14'][i] < data['EMA_50'][i] ) ) & ( data['Adj Close'][i] < data['EMA_8'][i] ) & ( data['STO_Signal'].iloc[i] == -2 ) ):
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

data["ATR"] = __ATR ( data, 14 )

data = __EMA ( data, 50 )
data = __EMA ( data, 14 )
data = __EMA ( data, 8 )
data = __STOCHASTIC (data, 14, 3)

if ( ( ( data["EMA_8"][-1]   > data["EMA_14"][-1] ) & ( data["EMA_8"][-1] > data["EMA_50"][-1] ) & ( data["EMA_14"][-1] > data["EMA_50"][-1] ) )
    &  ( data['Adj Close'][-1]   > data['EMA_8'][-1] )
    &  ( data['STO_Signal'].iloc[-1] == 2 ) ):
    print_log ( 'ema_8_14_50_atr_sto.py', 'LONG', [ 'EMA_8', 'EMA_14', 'EMA_50', 'STOCH' ] , backtest_strategy ( ticker , '2020-01-01' ) )

if ( ( ( data['EMA_8'][-1]     < data['EMA_14'][-1] ) and ( data['EMA_8'][-1] < data['EMA_50'][-1] ) and ( data['EMA_14'][-1] < data['EMA_50'][-1] ) )
    & (  data['Adj Close'][-1] < data['EMA_8'][-1] )
    &  ( data['STO_Signal'].iloc[-1] == -2 ) ):
    print_log ( 'ema_8_14_50_atr_sto.py', 'LONG', [ 'EMA_8', 'EMA_14', 'EMA_50', 'STOCH' ] , backtest_strategy ( ticker , '2020-01-01' ) )

