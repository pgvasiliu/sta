#!/usr/bin/env python3
# IMPORTING PACKAGES

import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
from termcolor import colored as cl
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

def __KC(dataframe, period=20, multiplier=2):
    """
    Calculates the Keltner Channels for a given DataFrame.

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the OHLC data of the asset.
    period (int): Period to calculate the Keltner Channels (default: 20).
    multiplier (float): Multiplier for the Average True Range (ATR) (default: 2).

    Returns:
    pd.DataFrame: A new DataFrame containing the Keltner Channels for the given OHLC data.
    """

    atr_lookback = 10

    tr = pd.DataFrame()
    tr['h_l'] = dataframe['High'] - dataframe['Low']
    tr['h_pc'] = abs(dataframe['High'] - dataframe['Close'].shift())
    tr['l_pc'] = abs(dataframe['Low'] - dataframe['Close'].shift())
    tr['tr'] = tr[['h_l', 'h_pc', 'l_pc']].max(axis=1)

    atr = tr['tr'].rolling(atr_lookback).mean()
    #atr = tr['tr'].ewm(alpha = 1/atr_lookback).mean()

    kc_middle = dataframe['Close'].rolling(period).mean()
    kc_upper = kc_middle + multiplier * atr
    kc_lower = kc_middle - multiplier * atr

    dataframe['KC_upper'] = kc_upper
    dataframe['KC_middle'] = kc_middle
    dataframe['KC_lower'] = kc_lower
    return dataframe

symbol = 'AAPL'
data = yf.download( symbol, start='2020-01-01', progress=False)

data = __SMA ( data, 20 )
data = __BB ( data, 20 )
data = __KC ( data, 20, 2 )


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)


plot_data = data[data.index >= '2020-01-01']

plt.plot(plot_data['Close'], linewidth = 2.5, label = 'AAPL')
plt.plot(plot_data['BB_upper'], label = 'UPPER BB 20', linewidth = 2, color = 'violet')
plt.plot(plot_data['BB_lower'], label = 'LOWER BB 20', linewidth = 2, color = 'violet')
plt.plot(plot_data['KC_upper'], linewidth = 2, color = 'orange', label = 'KC UPPER 20')
plt.plot(plot_data['KC_lower'], linewidth = 2, color = 'orange', label = 'KC LOWER 20')
plt.legend(fontsize = 15)
plt.title(f'{symbol} BOLINGER BANDS and KELTNER CHANNEL 20')

#plt.show()
plt.savefig ('_plots/' + symbol + '_BB_KC_simple.png')
