#!/usr/bin/env python3

#!/usr/bin/env python3

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


def __EMA ( data, n=9 ):
    data['EMA_{}'.format(n)] = data['Adj Close'].ewm(span = n ,adjust = False).mean()
    return data

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):
    """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
        The TradingView code is as follows:
        //@version=4
        study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
        len = input(14, minval=1, title="Length")
        src = input(close, "Source", type = input.source)
        up = rma(max(change(src), 0), len)
        down = rma(-min(change(src), 0), len)
        rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
        plot(rsi, "RSI", color=#8E1599)
        band1 = hline(70, "Upper Band", color=#C0C0C0)
        band0 = hline(30, "Lower Band", color=#C0C0C0)
        fill(band1, band0, color=#9915FF, transp=90, title="Background")
    :param data:
    :param window:
    :param round_rsi:
    :return: an array with the RSI indicator values
    """

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

def __MACD (data, m=12, n=26, p=9, pc='Adj Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])

    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data


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

    # EMA 20, 50
    data = __EMA (data, 6)
    data = __EMA (data, 9)
    data = __EMA (data, 12)
    data = __EMA (data, 21)
    data = __RSI ( data, 14 )
    data = __MACD ( data )

    histogram = data['MACD_HIST']

    latest_price = data['Adj Close'][-1]

    # Buy/sell signals for  SMA crosses
    data["Signal"] = 0.0

    data['Signal'] = np.select(
    [
        ((data["EMA_9"].shift(1) > data["EMA_21"].shift(1)) & (((histogram > 0) & (histogram.shift(1) < 0)) | ((histogram < 0) & (histogram.shift(1) > 0)))) | ((data["EMA_6"] > data["EMA_12"]) & (data["RSI_14"] > 50)),
        ((data["EMA_9"].shift(1) < data["EMA_21"].shift(1)) & (((histogram < 0) & (histogram.shift(1) > 0)) | ((histogram > 0) & (histogram.shift(1) < 0)))) | ((data["EMA_6"] < data["EMA_12"]) & (data["RSI_14"] < 50))
    ],
    [2, -2])

    data.index = pd.to_datetime(data.index)

    #print ( data.tail ( 60 ))

    # Plot the trading signals
    plt.figure(figsize=(14,7))

    plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 1,                  label = symbol,  )
    plt.plot ( data["EMA_6"], alpha = 0.6, linewidth = 1, color='orange',  label = 'EMA_6',  )
    plt.plot ( data["EMA_9"], alpha = 0.6, linewidth = 1, color='#FF006E', label = 'EMA_9' )
    #plt.plot ( data["EMA_12"], alpha = 0.6, linewidth = 2, color='blue',  label = 'EMA_12',  )
    #plt.plot ( data["EMA_21"], alpha = 0.6, linewidth = 2, color='green', label = 'EMA_21' )

    plt.plot ( data.loc[data["Signal"] ==  2.0].index, data["Adj Close"][data["Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
    plt.plot ( data.loc[data["Signal"] == -2.0].index, data["Adj Close"][data["Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

    plt.legend(loc = 'upper left')
    plt.title(f'{symbol}_{filename}')

    plt.xticks(rotation=45)
    plt.grid(True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    #plt.show()

    filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration


