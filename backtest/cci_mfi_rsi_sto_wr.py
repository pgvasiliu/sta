#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd
import numpy as np

import os, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def append_to_log(logfile, line):
    with open(logfile, 'a') as file:
        file.write(line + '\n')

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Adj Close'].rolling(window=n).mean()
    return data

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Adj Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: np.abs(x - x.mean()).mean())

    df['CCI_20'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)


    cci_upper_level  =  100
    cci_lower_level  =  (-100)
    cci_window = 20

    df['CCI_Signal'] = np.select(
        [ ( df['CCI_{}'.format(cci_window)].shift(1) < cci_lower_level ) & ( df['CCI_{}'.format(cci_window)] > cci_lower_level ) ,
          ( df['CCI_{}'.format(cci_window)].shift(1) > cci_upper_level ) & ( df['CCI_{}'.format(cci_window)] < cci_upper_level ) ],
        [2, -2])

    return df

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Adj Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))


    wr_window      = 20
    wr_upper_level = -20
    wr_lower_level = -80

    # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
    data['WR_Signal'] = np.select(
         [ ( data['WR_{}'.format(wr_window)].shift(1) > wr_upper_level ) & ( data['WR_{}'.format(wr_window)] < wr_upper_level ),
           ( data['WR_{}'.format(wr_window)].shift(1) < wr_lower_level ) & ( data['WR_{}'.format(wr_window)] > wr_lower_level )],
         [-2, 2])

    return data

def __STOCHASTIC (df, k, d):
     temp_df = df.copy()
     # Set minimum low and maximum high of the k stoch
     low_min = temp_df["Low"].rolling(window=k).min()
     high_max = temp_df["High"].rolling(window=k).max()

     # Fast Stochastic
     temp_df['k_fast'] = 100 * (temp_df["Adj Close"] - low_min)/(high_max - low_min)
     temp_df['d_fast'] = temp_df['k_fast'].rolling(window=d).mean()

     # Slow Stochastic
     temp_df['STO_K'] = temp_df["d_fast"]
     temp_df['STO_D'] = temp_df['STO_K'].rolling(window=d).mean()

     temp_df = temp_df.drop(['k_fast'], axis=1)
     temp_df = temp_df.drop(['d_fast'], axis=1)

     sto_overbought       = 80
     sto_oversold         = 20

     temp_df['STO_Signal'] = np.select(
            [ ( ( temp_df['STO_K'] > sto_oversold )   & ( temp_df['STO_K'].shift(1) < sto_oversold ) ),
              ( ( temp_df['STO_K'] < sto_overbought ) & ( temp_df['STO_K'].shift(1) > sto_overbought ) )],
            [2, -2])
     return temp_df

def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):

    delta = data["Adj Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    data['RSI_Signal'] = np.select(
            [ ( data['RSI_{}'.format(window)] > 40 ) & ( data['RSI_{}'.format(window)].shift(1) < 40),
              ( data['RSI_{}'.format(window)] < 60)  & ( data['RSI_{}'.format(window)].shift(1) > 60)],
            [2, -2])

    return data


def __MFI ( data, window=14):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data['Adj Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data['MFI_{}'.format(window)] = mfi

    mfi_overbought = 80
    mfi_oversold = 20
    data['MFI_Signal'] = np.select(
            [ ( data['MFI_{}'.format(window)] > mfi_oversold )   & ( data['MFI_{}'.format(window)].shift(1) < mfi_oversold ),
            (   data['MFI_{}'.format(window)] < mfi_overbought)  & ( data['MFI_{}'.format(window)].shift(1) > mfi_overbought)],
            [2, -2])

    return data



def backtest_strategy(stock, start_date, logfile ):
    """
    Function to backtest a strategy
    """

    csv_file = "../data/{}_1d.csv".format( stock )

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
    data = __SMA (data, 20)
    data = __SMA (data, 50)
    data = __CCI ( data, 20 )
    data = __MFI ( data, 14 )
    data = __RSI ( data, 20 )
    data = __STOCHASTIC ( data, 14, 3 )
    data = __WR ( data, 20 )

    #print ( data.tail(60))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []


    # Loop through data
    for i in range(len(data)):
        go_long  = 0
        go_short = 0

        if ( data['CCI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['MFI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['RSI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['STO_Signal'][i] == 2 ):
            go_long += 1
        if ( data['WR_Signal'][i] == 2 ):
            go_long += 1

        if ( data['CCI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['MFI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['RSI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['STO_Signal'][i] == -2 ):
            go_short += 1
        if ( data['WR_Signal'][i] == -2 ):
            go_short += 1

        # Buy signal
        #if ( data['MFI_Signal'][i] == 2 and  (position == 0 )):
        if ( go_long >= 3 and  (position == 0 )):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        #elif ( data['MFI_Signal'][i] == -2 and  (position == 1 )):
        elif ( go_short >= 3 and ( position == 1 )):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.0f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.0f}%")


    tot = ((total_returns - 100000) / 100000) * 100
    tot = (f"{tot:.0f}")
    line = (f"{name:<25}{stock:>6}{tot:>6} %")
    append_to_log ( logfile, line)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
    parser.add_argument('-l', '--logfile',  required=True, type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date, args.logfile )

