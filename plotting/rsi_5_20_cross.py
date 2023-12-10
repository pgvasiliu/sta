#!/usr/bin/env python3

import argparse
import os
import datetime
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.dates as mdates

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

filename, ext = os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+', required=True, type=str, help='ticker')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:
    csv_file = "{}/data/{}_1d.csv".format(parent_dir, symbol)

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv(csv_file, index_col='Date')
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv(csv_file)

    # RSI 5, 20
    data = __RSI(data, 5)
    data = __RSI(data, 20)

    latest_price = data['Adj Close'][-1]

    data = data.tail(365)
    # Required otherwise year is 1970
    data.index = pd.to_datetime(data.index)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Plot Adj Close
    ax1.plot(data.index, data['Adj Close'], alpha=0.3, linewidth=2, label=symbol)
    ax1.set_ylabel('Adj Close')
    ax1.legend(loc='upper left')

    # Plot RSI
    ax2.plot(data.index, data["RSI_5"], alpha=0.6, linewidth=2, color='orange', label='RSI_5')
    ax2.plot(data.index, data["RSI_20"], alpha=0.6, linewidth=3, color='#FF006E', label='RSI_20')
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')

    # Buy/sell signals for RSI crosses
    data["RSI_5_20_Signal"] = np.select(
        [(data['RSI_5'].shift(1) < data['RSI_20'].shift(1)) & (data['RSI_5'] > data['RSI_20']),
         (data['RSI_5'].shift(1) > data['RSI_20'].shift(1)) & (data['RSI_5'] < data['RSI_20'])],
        [2, -2])

    # Plot the buy/sell signals on Adj Close plot
    ax1.scatter(data.loc[data["RSI_5_20_Signal"] == 2.0].index, data["Adj Close"][data["RSI_5_20_Signal"] == 2.0],
                marker='^', s=100, color="g", label='BUY SIGNAL')
    ax1.scatter(data.loc[data["RSI_5_20_Signal"] == -2.0].index, data["Adj Close"][data["RSI_5_20_Signal"] == -2.0],
                marker='v', s=100, color="r", label='SELL SIGNAL')

    ax1.set_title(f'{symbol}_{filename}')
    ax1.grid(True)
    ax2.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    ax1.text(0.05, 0.95, label, transform=ax1.transAxes, verticalalignment='bottom',
             bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    filename = "{}/plotting/_plots/{}_{}.png".format(parent_dir, symbol, filename)
    plt.savefig(filename)
    plt.clf()  # Clear the plot for the next iteration

