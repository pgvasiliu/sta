#!/usr/bin/env python3

# IMPORTING PACKAGES

import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from termcolor import colored as cl
from math import floor

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

import yfinance as yf


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


def __KC2 ( data, period=20, multiplier=2 ):

    atr_lookback = 10

    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift())
    tr3 = abs(data['Low'] - data['Close'].shift())

    frames = [tr1, tr2, tr3]

    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)

    atr = tr.ewm(alpha = 1/atr_lookback).mean()

    kc_middle = data['Close'].ewm(period).mean()
    kc_upper = data['Close'].ewm(period).mean() + multiplier * atr
    kc_lower = data['Close'].ewm(period).mean() - multiplier * atr

    data['KC_upper'] = kc_upper
    data['KC_middle'] = kc_middle
    data['KC_lower'] = kc_lower
    return data


plt.rcParams['figure.figsize'] = (20,10)
plt.style.use('fivethirtyeight')

symbol = 'AAPL'

data = yf.download ( symbol , start='2020-01-01', progress=False)
data = __KC ( data, 20, 2 )

# KELTNER CHANNEL PLOT
plt.plot ( data['Close'], linewidth = 2, label = symbol)
plt.plot ( data['KC_upper'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC UPPER 20')
plt.plot ( data['KC_middle'], linewidth = 1.5, color = 'grey', label = 'KC MIDDLE 20')
plt.plot ( data['KC_lower'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC LOWER 20')
plt.legend (loc = 'lower right', fontsize = 15)
plt.title (f'{symbol} KELTNER CHANNEL 20')

#plt.show()
plt.savefig ('_plots/' + symbol + '_KC_simple.png')

