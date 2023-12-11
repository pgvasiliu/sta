#!/usr/bin/env python3

#######################
#####  ATR BANDS  #####
#######################

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################
from util.atr        import __ATR

#def calculate_ATR(df_func):
#    # Calculating ATR - Average True Range
#    high_low = df_func['High'] - df_func['Low']
#    high_close = np.abs(df_func['High'] - df_func['Close'].shift())
#    low_close = np.abs(df_func['Low'] - df_func['Close'].shift())
#
#    ranges = pd.concat([high_low, high_close, low_close], axis=1)
#    true_range = np.max(ranges, axis=1)
#
#    df_func['ATR_14'] = true_range.rolling(14).sum()/14
#    
#    return df_func

# Define the ticker and download the historical data
ticker = 'AAPL'
data = yf.download(ticker, period='5y')
#data = data.drop(['Adj Close'], axis=1).dropna()

atr = __ATR ( data, 14 )

#data = calculate_ATR( data )

stop_loss_percent = 2 # Replace with desired stop-loss percentage
current_price = data["Adj Close"][-1]

stop_loss_level = current_price - (atr[-1] * (stop_loss_percent / 100))

print ( atr )

print(f"Current Price: {current_price:.2f}")
print(f"Stop Loss Level: {stop_loss_level:.2f}")

print ( data.tail(3))

