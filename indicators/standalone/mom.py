
import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd
import numpy as np

def __MOM (data, window=14):
    # Download the stock data using yfinance

    # Calculate the Momentum (MOM) indicator
    mom = pd.Series(data["Adj Close"]).diff(window)

    # Add the MOM indicator to the DataFrame
    data["MOM"] = mom

    return data

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:

    csv_file = "../../data/{}_1d.csv".format( symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date', parse_dates=True )
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    window_mom = 14

    # Calculate the MOM indicator and print the current value
    data = __MOM ( data , window_mom )
    current_mom = data["MOM"].iloc[-1]

    print("Current MOM value for", symbol, "is:", current_mom)


