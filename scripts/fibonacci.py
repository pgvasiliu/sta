#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd

import numpy as np

import os, sys, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

pd.set_option('display.precision', 2)
pd.set_option('display.float_format', '{:.2f}'.format)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Environment settings:
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)

def camarilla_fib(df):
    high = df['High'].iloc[-1]
    low = df['Low'].iloc[-1]
    range_ = high - low
    fib_levels = {'PP': round(low + (range_ * 1.1/2), 2),
                  'S1': round(low + (range_ * 1.1/6), 2),
                  'S2': round(low + (range_ * 1.1/3), 2),
                  'S3': round(low + (range_ * 1.1/2), 2),
                  'R1': round(low + (range_ * 1.1 * 2/3), 2),
                  'R2': round(low + (range_ * 1.1 * 5/6), 2),
                  'R3': round(high, 2)}
    return fib_levels

def woodie_fib(df):
    high = df['High'].iloc[-1]
    low = df['Low'].iloc[-1]
    range_ = high - low
    fib_levels = {'PP': round(low + (range_ * 1/2), 2),
                  'S1': round(low + (range_ * 1/4), 2),
                  'S2': round(low + (range_ * 1/3), 2),
                  'S3': round(low + (range_ * 0.382), 2),
                  'R1': round(low + (range_ * 0.618), 2),
                  'R2': round(low + (range_ * 2/3), 2),
                  'R3': round(high, 2)}
    return fib_levels

def classic_fib(df):
    high = df['High'].iloc[-1]
    low = df['Low'].iloc[-1]
    range_ = high - low
    fib_levels = {'PP': round(low + (range_ * 1/2), 2),
                  'S1': round(low + (range_ * 0.236), 2),
                  'S2': round(low + (range_ * 0.382), 2),
                  'S3': round(low + (range_ * 0.5), 2),
                  'R1': round(low + (range_ * 0.618), 2),
                  'R2': round(low + (range_ * 0.764), 2),
                  'R3': round(high, 2)}
    return fib_levels

def demark_fib(df):
    high = df['High'].iloc[-1]
    low = df['Low'].iloc[-1]
    range_ = high - low
    fib_levels = {'S1': round(low + (range_ * 0.382), 2),
                  'S2': round(low + (range_ * 0.5), 2),
                  'S3': round(low + (range_ * 0.618), 2),
                  'R1': round(low + (range_ * 0.236), 2),
                  'R2': round(low + (range_ * 0.191), 2)}
    return fib_levels

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', required=True, help='Stock ticker symbol')
parser.add_argument('-f', '--fib', choices=['camarilla', 'woodie', 'classic', 'demark'], default='camarilla',
                    help='Fibonacci name to use (default: camarilla)')
args = parser.parse_args()


file_list = [ "./data/{}_1d.csv".format( args.ticker ), "../data/{}_1d.csv".format( args.ticker ) ]
for item in file_list:
    if os.path.exists(item):
      csv_file = item

# Get today's date
today = datetime.datetime.now().date()

# if the file was downloaded today, read from it
if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
    data = pd.read_csv ( csv_file, index_col='Date' )
else:
    # Download data
    start_date = "2020-01-01"
    data = yf.download( args.ticker, start=start_date, progress=False)
    #data.to_csv ( csv_file )


# Select the last row of the dataframe
last_row = data.iloc[[-1]]

# Calculate FIB levels based on the selected Fibonacci name and add them to the last row
fib_function_map = {'camarilla': camarilla_fib, 'woodie': woodie_fib, 'classic': classic_fib, 'demark': demark_fib}
fib_function = fib_function_map[args.fib]
fib_levels = fib_function(last_row)
fib_data = pd.DataFrame(fib_levels, index=[0])

# Update the column names with Fibonacci levels
fib_data.columns = [f"{args.fib.capitalize()}_{level}" for level in fib_data.columns]


# Calculate the closest Fibonacci level to the current price
current_price = last_row['Adj Close'].iloc[0]
closest_fib_level = min(fib_levels, key=lambda x: abs(fib_levels[x] - current_price))

# Get the name and value of the closest Fibonacci level
fib_level_name = f"{args.fib.capitalize()}_{closest_fib_level}"
fib_level_value = fib_levels[closest_fib_level]

# Print the closest Fibonacci level, its name, value, and the current price

# Print the last dataframe with the selected Fibonacci name and formatted floats
#print(f"\n{args.ticker} 1d ---> INFO (FIB) {args.fib.capitalize()} FIB Levels")
print(f"{args.ticker} 1d ---> INFO (FIB) {args.fib.capitalize()} Price: {current_price:.2f}, closest {fib_level_name} ({fib_level_value})")
pd.set_option('display.float_format', '{:.2f}'.format)  # Set float formatting to 2 decimal places
print(fib_data)


sys.exit(0)

