#!/usr/bin/env python3

import argparse

import os, datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

import yfinance as yf

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data

def __BB (data, window=20):
    std = data['Close'].rolling(window).std()
    data = __SMA ( data, window )
    data['BB_upper']   = data["SMA_20"] + std * 2
    data['BB_lower']   = data["SMA_20"] - std * 2
    data['BB_middle']  = data["SMA_20"]

    return data

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
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

    return data


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

filename, ext =  os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
parser.add_argument('-c', '--csv_file', required=True,  type=str, help='csv_file')
parser.add_argument('-i', '--interval', required=True,  type=str, help='interval')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)



def implement_strategy(prices, low, rsi ):
    buy_price = []
    sell_price = []
    strategy_signal = []
    signal = 0

    for i in range(len(prices)):
        if ( prices.iloc[i] < low.iloc[i] ) and ( rsi.iloc[i] < 30 ):
            if signal != 1:
                buy_price.append(prices.iloc[i])
                sell_price.append(np.nan)
                signal = 1
                strategy_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                strategy_signal.append(0)
        elif  ( rsi.iloc[i] > 70 ):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices.iloc[i])
                signal = -1
                strategy_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                strategy_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            strategy_signal.append(0)

    return buy_price, sell_price, strategy_signal

for symbol in args.ticker:

    filename, ext =  os.path.splitext(os.path.basename(__file__))

    if not os.path.exists(args.csv_file):
        # Get stock data from Yahoo Finance
        data = yf.download(symbol, start='2020-01-01', interval=args.interval, progress=False, threads=True )
        data.to_csv ( '{}'.format ( args.csv_file ) )


    # If the csv file is older than 1440 ( 24h * 60min )        
    today = datetime.datetime.now().date()
    if os.path.exists(args.csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(args.csv_file)) > datetime.timedelta(minutes=1440))(args.csv_file):
        # Get stock data from Yahoo Finance
        data = yf.download(symbol, start='2020-01-01', interval=args.interval, progress=False, threads=True )
        data.to_csv ( '{}'.format ( args.csv_file ) )
            
    data = pd.read_csv ( args.csv_file, index_col='Date' )

    data = __SMA ( data, 20 )
    data = __BB ( data, 20 )
    data = __RSI ( data, 14 )

    data = data.dropna()
    data = data.tail(365)


    latest_price = data['Adj Close'].iloc[-1]
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)
    
    buy_price, sell_price, strategy_signal = implement_strategy( data['Adj Close'], data['BB_lower'], data['RSI_14'])

    ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

    ax1.plot ( data['Adj Close'], linewidth = 2)
    ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
    ax1.legend()
    ax1.set_title(f'{symbol} {filename } TRADING SIGNALS')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.05, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    ax2.plot ( data['Adj Close'], linewidth = 2, color = 'skyblue', label = 'Adj Close')
    ax2.set_title(f'{symbol} BolingerBands Close')
    ax2.legend()
    ax2.plot ( data['BB_upper'], label = 'UPPER BB 20', linestyle = '--', linewidth = 1, color = 'black')
    ax2.plot ( data['SMA_20'],   label = 'MIDDLE BB 20',linestyle = '--', linewidth = 1.2, color = 'grey')
    ax2.plot ( data['BB_lower'], label = 'LOWER BB 20', linestyle = '--', linewidth = 1, color = 'black')
    ax2.text(0.05, 0.05, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})


    #plt.show()
    SAVE_TO = "{}/plotting/_plots/{}/{}".format ( parent_dir, symbol, args.interval ) 
    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO, exist_ok=True)
    filename = "{}/{}_{}.png".format ( SAVE_TO, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration
