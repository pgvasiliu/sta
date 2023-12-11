#!/usr/bin/env python3

import argparse

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

import os, datetime

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    for symbol in args.ticker:

        filename, ext =  os.path.splitext(os.path.basename(__file__))

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

        data = data.dropna()
        data.index = pd.to_datetime(data.index)

        latest_price = data['Adj Close'][-1]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
        plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

        plt.plot ( data.index, data['Adj Close'])
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.title(f'{symbol} Adj Closing Price')

        plt.xticks(rotation=45)
        plt.grid(True)

        #plt.show()
        filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
        plt.savefig ( filename )
        plt.clf()  # Clear the plot for the next iteration

