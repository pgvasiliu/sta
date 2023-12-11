#!/usr/bin/env python3

import argparse

import os,sys,datetime

import yfinance as yf
import pandas as pd
import numpy as np

#def cci(data, ndays):
#    TP = (data['High'] + data['Low'] + data['Adj Close']) / 3
#    CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()), name = 'CCI')
#    return CCI

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Adj Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    #df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: np.abs(x - x.mean()).mean())

    df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df['CCI_CrossOverBought'] = np.where ( ( df['CCI'].shift(1) < 100)  & ( df['CCI'] >= 100),  1, 0 )
    df['CCI_CrossOverSold']   = np.where ( ( df['CCI'].shift(1) > -100) & ( df['CCI'] <= -100), 1, 0 )

    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    return df

#def calculate_levels(data, ndays):
#    data['CCI'] = cci(data, ndays)
#    data['CCI_Overbought'] = np.where(data['CCI'] > 100, 1, 0)
#    data['CCI_Oversold'] = np.where(data['CCI'] < -100, 1, 0)
#    data['CCI_CrossOver'] = np.where((data['CCI'] > 0) & (data['CCI'].shift(1) < 0), 1, 0)
#    data['CCI_CrossUnder'] = np.where((data['CCI'] < 0) & (data['CCI'].shift(1) > 0), 1, 0)
#    return data

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

    # Calculate the CCI and levels
    data = __CCI (data, 20)
    #data["CCI_prev"] = data["CCI"].shift(1)

    yesterday_cci = data['CCI'][-2]
    today_cci     = data['CCI'][-1]


    if data['CCI_CrossOverBought'].iloc[-1] == 1:
        print(f'CCI HOLD :: {ticker} has crossed OverBought level.')
    if data['CCI_CrossOverSold'].iloc[-1] == 1:
        print(f'CCI HOLD :: {ticker} has crossed OverSold level.')


    if ( today_cci > yesterday_cci ) and ( today_cci > 100 ) and ( yesterday_cci > 100 ):
        print(f'CCI SELL :: {ticker} is continuing to be OverBought')
    if ( today_cci < yesterday_cci ) and ( today_cci < -100 ) and ( yesterday_cci < 100 ):
        print(f'CCI BUY :: {ticker} is continuing to be OverSold')


    if ( today_cci < yesterday_cci ) and ( today_cci < 100 ) and (yesterday_cci > 100 ):
        print(f'CCI STRONG SELL :: {ticker} is going down!')
    if ( today_cci > yesterday_cci ) and ( today_cci > -100 ) and ( yesterday_cci < -100 ):
        print(f'CCI STRONG BUY :: {ticker} is going UP!')


    # Print the last 5 rows of the data to check the results
    print(data.tail(5))

