#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore")

import argparse

import os, datetime

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import matplotlib.dates as mdates

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

def __SRSI ( data, period=14, SmoothD=3, SmoothK=3):
    # RSI
    data = __RSI ( data, period)

    # Stochastic RSI
    stochrsi  = (data['RSI_14'] - data['RSI_14'].rolling(period).min()) / (data['RSI_14'].rolling(period).max() - data['RSI_14'].rolling(period).min())
    data['SRSI'] = stochrsi
    data['SRSI_K'] = stochrsi.rolling(SmoothK).mean() * 100
    data['SRSI_D'] = data['SRSI_K'].rolling(SmoothD).mean()
    return data

def implement_strategy (prices, SRSI_K, SRSI_D):
    buy_price = []
    sell_price = []
    srsi_signal = []
    signal = 0

    for i in range(len(prices)):
        if ( SRSI_K[i] > 20 and SRSI_D[i] > 20 ):
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                srsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                srsi_signal.append(0)
        elif ( SRSI_K[i] < 80 and SRSI_D[i] < 80 ):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                srsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                srsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            srsi_signal.append(0)

    return buy_price, sell_price, srsi_signal

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

filename, ext =  os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:

    csv_file = "{}/data/{}_1d.csv".format( parent_dir, symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download ( symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    data = __SRSI ( data, period=14, SmoothD=3, SmoothK=3 )
    latest_price = data['Adj Close'][-1]

    data = data.tail(365)
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    buy_price, sell_price, srsi_signal = implement_strategy ( data['Adj Close'], data['SRSI_K'], data['SRSI_D'])

    # TSI PLOT
    ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

    ax1.plot ( data['Adj Close'], linewidth = 2)
    ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
    ax1.legend()
    ax1.set_title(f'{symbol} SRSI TRADING SIGNALS')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.95, label, transform=ax1.transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    ax2.plot ( data['SRSI_K'], linewidth = 2, color = 'orange', label = 'SRSI_K')
    ax2.plot ( data['SRSI_D'], linewidth = 2, color = '#FF006E', label = 'SRSI_D')
    ax2.set_title(f'{symbol} SRSI')
    ax2.legend()

    ax2.text(s='Overbought', x=data.index[30], y=80, fontsize=14)
    ax2.text(s='Oversold', x=data.index[30], y=20, fontsize=14)
    ax2.axhline(y=80, color='red')
    ax2.axhline(y=20, color='green')

    plt.xticks(rotation=45)
    plt.grid(True)


    filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration

