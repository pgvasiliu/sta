#!/usr/bin/env python3

import argparse

import os,sys,datetime
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

# def __SMA ( df['Close'], 21 )
from util.sma   import __SMA

#def __BB (df, window=20):
from util.bolinger_bands   import __BB

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:

    csv_file = "../data/{}_1d.csv".format( symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date', parse_dates=True )
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    bb_window = 20

    # Calculate the Bollinger Bands for the stock data
    data = __BB ( data, bb_window)


    # keep 2 decimals
    #data['BB_upper'] = data['BB_upper'].apply(lambda x: float("{:.2f}".format(x)))
    #data['BB_lower'] = data['BB_lower'].apply(lambda x: float("{:.2f}".format(x)))

    # Calculate the cross over and cross under values
    bb_cross_over  = np.where ( data['Adj Close'] > data['BB_upper'], 1, 0 )
    bb_cross_under = np.where ( data['Adj Close'] < data['BB_lower'], 1, 0 )

    # Add cross over and cross under columns to the dataframe
    #data['BB_Cross_Over']  = bb_cross_over
    #data['BB_Cross_Under'] = bb_cross_under


    # Print the dataframe
    print( data.tail (5) )

    # Check for the crossunder and crossover conditions
    if data['BB_Cross_Over'].iloc[-1] == 1:
        print("BB [SELL] Stock has crossed over bolinger band on the upside")
    elif data['BB_Cross_Under'].iloc[-1] == 1:
        print("BB [BUY] Stock has crossed under bolinger band on the downside")
    else:
        print("No conditions are met")

    #data.plot(y=['Adj Close', 'BB_upper', 'BB_middle', 'BB_lower'])
    #plt.title('Apple Close Prices & Bollinger Bands BB(20,2)')
    #plt.legend(loc='upper left')
    #plt.show()

