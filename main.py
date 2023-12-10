#!/usr/bin/env python3
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# pylint: disable=C0122
# isort: skip_file



try:
    import os,sys
    import argparse
    import time
    import datetime
    import json
    import requests
    import yfinance as yf
    import numpy as np
    import pandas as pd
    import bisect
except ModuleNotFoundError or ImportError as ee:
    print('Error importing python module: {0}'.format(ee.msg), file=sys.stderr)
    sys.exit(1)
except Exception as ee:
    print(ee)

import subprocess

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

# disable SSL cert warn
#from urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import logging
#logging.basicConfig(level=logging.INFO)

#####################################
#####  DEPENDENCIES / Includes  #####
#####################################
sys.path.insert(0, './utils')

# def __WR (df, period):
from util.wr     import __WR

# def __TEMA (df, period):
from util.tema   import __TEMA

# def __STOCHASTIC (df, k, d):
from util.stochastic import __STOCHASTIC

# def __RSI (df, window=14):
from util.rsi   import __RSI

# def __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3):
from util.stochastic_rsi import __STOCHASTIC_RSI

# def __SMA (df, n=5):
from util.sma   import __SMA

# def __EMA (df, window=9):
from util.ema   import __EMA

# def __DWMA ( data, window=9)
from util.dwma   import __DWMA

from util.emav   import __EMAV

# def __WSMA ( data, window=20 )
from util.wsma   import __WSMA

# def __CCI (df, window=20):
from util.cci   import __CCI

# def __BB (df, window=20):
from util.bolinger_bands   import __BB

# def __MACD (data, m=12, n=26, p=9, pc='Close'):
from util.macd   import __MACD

# def __KDJ (df)
from util.kdj   import __KDJ

from util.kc   import __KC

# def __ATR_bands ( data, t=14 ):
from util.atr_bands import __ATR_BANDS

from util.atr        import __ATR
from util.atr        import calculate_ATR

# def __CMO ( data, period )
from util.cmo import __CMO

# def __MFI ( data, window=14 )
from util.mfi   import __MFI

# def __CMF ( data, window=20 )
from util.cmf import __CMF

# def __ADX ( data, lookback )
from util.adx import __ADX

# def __MOM ( data, window=14 )
from util.mom import __MOM

# def __AO ( data, window_1, window_2 )
from util.ao import __AO

# def __TSI ( data, long, short, signal)
from util.tsi import __TSI

# def __ROC (data, n=12, m=6)
from util.roc  import __ROC


# def __PSAR (data, iaf = 0.02, maxaf = 0.2)
from util.psar  import __PSAR

# def WMA ( data, window)
from util.wma   import WMA



from util.candles import hammer

from util.support import isSupport, isResistance, sr

def find_position(numbers, target):
    numbers = [float(num) for num in numbers]  # Convert string numbers to floats
    index = bisect.bisect_left(numbers, target)
    if index == 0:
        return "Number is less than all elements in the list."
    elif index == len(numbers):
        return "Number is greater than all elements in the list."
    else:
        lower_number = numbers[index-1]
        upper_number = numbers[index]

        percentage_lower = (target - lower_number) / (upper_number - lower_number) * 100
        percentage_lower = round ( percentage_lower, 2 )

        percentage_upper = 100 - percentage_lower
        percentage_upper = round ( percentage_upper, 2 )

        return f"                             {target} is between {lower_number} ( {percentage_lower:.2f} %  away)  and {upper_number} ( {percentage_upper:.2f} %  away )"


def find_position_in_dictionary(dictionary, number):
    # Convert string values to float values
    float_dict = {k: float(v) for k, v in dictionary.items()}

    # Sort the dictionary values
    sorted_values = sorted(float_dict.values())

    # Find the two values between which the number is positioned
    lower_value = None
    upper_value = None

    for value in sorted_values:
        if value <= number:
            lower_value = value
        else:
            upper_value = value
            break

    # Calculate the percentage distance
    if lower_value is None:
        lower_percentage = 0.0
        upper_percentage = 100.0
    elif upper_value is None:
        lower_percentage = 100.0
        upper_percentage = 0.0
    else:
        lower_distance = number - lower_value
        upper_distance = upper_value - number
        total_distance = upper_value - lower_value

        lower_percentage = (lower_distance / total_distance) * 100
        upper_percentage = (upper_distance / total_distance) * 100

    return lower_value, upper_value, lower_percentage, upper_percentage




def send_discord_message(webhook_url, ticker, title, description):
    # Construct the message payload with a title and a blue color
    message = {
        "username": "Stock Bot",
        "embeds": [
            {
                "title": "```" + ticker + " ::: " + title + "```",
                "description": f"{ticker}: {description}",
                "color": 3447003,
                "footer": {
                    "text": "Powered by Stock Bot",
                    "icon_url": "https://cdn.iconscout.com/icon/free/png-512/stock-market-282161.png"
                }
            }
        ]
    }

    #message["embeds"][0]["description"] = message["embeds"][0]["description"].replace(f"{ticker}:", f"```fix\n{ticker}\n```")
    
    # Send the message to the webhook URL using the requests library
    response = requests.post(webhook_url, json=message)

    # Check if the request was successful
    if response.status_code != 204:
        print(f"Error sending message: {response.content}")


#            Period           Interval              Sleep before refresh data
TIMEFRAMES = {
    "1m":  { "Period": "7d",   "Interval": "1m",    "Refresh": "60"   },
    "5m":  { "Period": "30d",  "Interval": "5m",    "Refresh": "60"  },
    "15m": { "Period": "30d",  "Interval": "15m",   "Refresh": "60"  },
    "30m": { "Period": "60d",  "Interval": "30m",   "Refresh": "600"  },
    "90m": { "Period": "60d",  "Interval": "90m",   "Refresh": "900"  },
    "1h":  { "Period": "730d", "Interval": "1h",    "Refresh": "1200" },
    "1d":  { "Period": "5y",   "Interval": "1d",    "Refresh": "1800" },
    "5d":  { "Period": "5y",   "Interval": "5d",    "Refresh": "14000"},
    "1wk": { "Period": "5y",   "Interval": "1wk",   "Refresh": "86400"},
    "1mo": { "Period": "5y",   "Interval": "1mo",   "Refresh": "86400"},
    "3mo": { "Period": "5y",   "Interval": "3mo",   "Refresh": "86400"}

}

settings = {
    "enable_debug": 0,
    "enable_discord": 0,
    "enable_slack": 0
}

#Discord Webhook URL
discord_env = {
    "PROD": 'https://discord.com/api/webhooks/1026327480900014162/YPhlm0QMkHoOZXmpL2IC1BPwIIWBBm3MEzW02RYHu4yNyYMVOfRXDI8sfkV5HXCjuITG',
    "DEV": 'https://discord.com/api/webhooks/1026327480900014162/YPhlm0QMkHoOZXmpL2IC1BPwIIWBBm3MEzW02RYHu4yNyYMVOfRXDI8sfkV5HXCjuITG'
}
discord_url = discord_env['DEV']


parser = argparse.ArgumentParser(description='Script that monitors a number of tickers')

# Add a positional argument for the time interval
parser.add_argument('-i', '--interval', type=str, required=True, help='time interval i.e. one of 1m, 5m, 15m, 30m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo')

# log file
parser.add_argument('-l', '--logfile', type=str, required=False, help='log file i.e. app.log')

# Add a positional argument for a list of stocks
parser.add_argument('-t', '--tickers', type=str, nargs='+', required=True, help='list of stock tickers')

# Add a positional argument for a strategy
parser.add_argument('-s', '--strategies', type=str, nargs='+', required=False, help='load named strategies from strategie/ folder')

# Add a positional argument for a strategy
parser.add_argument('-r', '--refresh', type=str, required=False, help='override default refresh settings, in seconds')

# Add a positional argument for displaying strategy percentage
parser.add_argument('-p', '--percentage', type=int, required=False, help='use strategies that return more than %%')

# Parse the command-line arguments
args = parser.parse_args()


strategies = {}
indicators = {}
counter = 0

period   = TIMEFRAMES[args.interval]['Period']
interval = TIMEFRAMES[args.interval]['Interval']
refresh  = TIMEFRAMES[args.interval]['Refresh']

if ( args.logfile ):
    append_to = args.logfile
else:
    append_to = "app.log"
logging.basicConfig(filename=append_to, filemode='a', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# 'Close' or 'Adj Close' ?
#cl='Adj Close'
cl='Close'

for ticker in args.tickers:
    strategies[ticker] = []
    indicators[ticker] = []


while True:

    def print_log ( strategy_name, long_short='LONG', perc=0, *ind):
        my_list = sorted ( set ( strategies[ticker] ) )

        spath = "plotting/{}".format ( strategy_name )
        if ( os.path.exists ( spath )):
            command = ['python3', spath, '-t', ticker]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                # Check if the command was successful
                #if result.returncode == 0:
                #    # Print the output on the screen
                #    print(result.stdout)
                #else:
                #    # Print an error message
                #    print("Error:", result.stderr)
            except subprocess.CalledProcessError as e:
                print(f"Script execution failed with error:\n{e.stderr}")

        #print ( my_list )
        if strategy_name not in my_list:
            number = int(''.join(filter(str.isdigit, ind[0])))

            if ( args.percentage ):
                if ( number >= args.percentage ):
                    message = f"{ticker} {interval} ---> {long_short} ::: {strategy_name} ::: return {number} ::: {perc}"
                    logging.warning(message)
                    strategies[ticker].append(strategy_name)
                    #indicators[ticker].extend ( ind )
                    print ( f"{message}")
            else:
                message = f"{ticker} {interval} ---> {long_short} ::: {strategy_name} ::: return {number} ::: {perc}"
                logging.warning(message)
                strategies[ticker].append(strategy_name)
                #indicators[ticker].extend ( ind )
                print ( f"{message}")

            if ( settings['enable_discord'] ):
                discord_message = '  {:8s}  {:10s}   {:8s}%  {:30s} '.format ( ticker, "NA" , "NA", message )
                send_discord_message (discord_url, ticker, long_short, discord_message)

    counter += 1
    print ("-------------------------  %d  -------------------------" % counter) 

    # Use the list of stocks and integer value in the script
    for ticker in args.tickers:

        #my_list = list ( set ( strategies[ticker] ))
        discord_message = ''


        now = datetime.datetime.now()


        # Get stock data from Yahoo Finance
        data = yf.download(ticker, period=period, interval = interval, progress=False, threads=True )
        #data['CL'] = data['Close'].copy()
        data.to_csv('data/{}_1d.csv'.format ( ticker ), float_format='%.2f')

        # We need to fetch daily data in order to get strategy return numbers
        if ( period != '1d' ):
            data_1d = yf.download ( ticker, start='2020-01-01', progress=False, threads=True )


        # Current price, percentage from the previous day

        current_price = data["Close"][-1]
        current_price = round ( current_price, 2 )

        # Get the price change percentage from the previous day
        previous_close_price = data["Close"][-2]

        price_change_percentage = ((current_price - previous_close_price) / previous_close_price) * 100
        price_change_percentage = round(price_change_percentage, 2)  # Round to 2 decimal places

        info = " [ {}  {} % ] ".format ( current_price, price_change_percentage )
        print ( "=====  " + ticker + info + "  =====  " + now.strftime("%Y-%m-%d %H:%M:%S") + "  =====" )


        # FIBONACCI #
        with open ( 'util/fib.py') as f: exec(f.read())


        fib_path = "scripts/fibonacci.py"
        fib_name = 'camarilla'

        if ( os.path.exists ( fib_path )):
            command = ['python3', fib_path, '-t', ticker, '-f', fib_name]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                # Check if the command was successful
                if result.returncode == 0:
                    # Print the output on the screen
                    print(result.stdout)
                else:
                    # Print an error message
                    print("Error:", result.stderr)
            except subprocess.CalledProcessError as e:
                print(f"Script execution failed with error:\n{e.stderr}")

        #####  FIB !!!  #####
        print ( "%s 1d --->  INFO  (FIBs)     ---> %s" % ( ticker, fib ( data ) ) )
        lower, upper, lower_percentage, upper_percentage = find_position_in_dictionary ( fib ( data ), current_price)
        print (f"                            FIB  Lower value: {lower}, {lower_percentage:.2f} %  away")
        print (f"                            FIB  Upper value: {upper}, {upper_percentage:.2f} %  away")
        print ()

        #####  Support and R !!!  #####
        #print ( "         [%s] FIBs CAM ---> %s" % ( symbol,  pivot_levels(_open, _high, _low, _close) ) )
        #print ( "         [%s] ATR_band ---> (LOW %.2f, %.2f%% away )   CUR %s   (MAX %.2f, %.2f%% away)" % ( symbol, atr_band_lower, 100 - ( atr_band_lower * 100 / price ), price_string, atr_band_higher, 100 - ( price * 100 / atr_band_higher  ) ) )
        print ( "%s 1d ---> INFO (SupplyRes)   ---> %s" % ( ticker, sr ( data ) ) )
        position = find_position( sr ( data ), current_price )
        print ( position )
        print ()


        data['Fibonacci_0.236'] = data[cl].shift(0) * 0.236
        data['Fibonacci_0.382'] = data[cl].shift(0) * 0.382
        data['Fibonacci_0.50']  = data[cl].shift(0) * 0.50
        data['Fibonacci_0.618'] = data[cl].shift(0) * 0.618
        data['Fibonacci_1.00']  = data[cl].shift(0) * 1.00
        data['Fibonacci_1.27']  = data[cl].shift(0) * 1.27
        data['Fibonacci_1.618'] = data[cl].shift(0) * 1.618

        data['candle_size'] = ( data[cl] - data['Open'] ) * ( data[cl] - data['Open'] ) / 2

        data = hammer ( data )

        #########  SMA 5, 8  #####
        for i in [ 3, 5, 8, 9, 19, 20, 21, 50, 100, 200]:
            data = __SMA ( data, i, cl=cl )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['SMA_5_8_Signal'] = np.select(
            [ ( data['SMA_5'] > data['SMA_8'] ) & ( data['SMA_5'].shift(1) < data['SMA_8'].shift(1) ),
            (   data['SMA_5'] < data['SMA_8'] ) & ( data['SMA_5'].shift(1) > data['SMA_8'].shift(1) )],
            [2, -2])

        data['SMA_20_50_Signal'] = np.select(
            [ ( data['SMA_20'] > data['SMA_50'] ) & ( data['SMA_20'].shift(1) < data['SMA_20'].shift(1) ),
            (   data['SMA_20'] < data['SMA_50'] ) & ( data['SMA_20'].shift(1) > data['SMA_50'].shift(1) )],
            [2, -2])

        # Trend indicator
        #data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()
        data['Trend_20']  = data[cl] / data['SMA_20']
        data['Trend_50']  = data[cl] / data['SMA_50']
        data['Trend_100'] = data[cl] / data['SMA_100']
        data['Trend_200'] = data[cl] / data['SMA_200']

        #########  EMA 9, 21  #####
        for i in [ 5, 8, 9, 20, 21, 50, 100, 200]:
           data = __EMA ( data, i, cl )

        # CROSS_over / CROSS_under ::: 2 = LONG, -2 = SHORT
        data['EMA_20_50_Signal'] = np.select(
            [ ( data['EMA_20'] > data['EMA_50'] ) & ( data['EMA_20'].shift(1) < data['EMA_50'].shift(1) ) ,
              ( data['EMA_20'] < data['EMA_50'] ) & ( data['EMA_20'].shift(1) > data['EMA_50'].shift(1) ) ],
            [2, -2])

        data['EMA_9_21_Signal'] = np.select(
            [ ( data['EMA_9'] > data['EMA_21'] ) & ( data['EMA_9'].shift(1) < data['EMA_21'].shift(1) ) ,
              ( data['EMA_9'] < data['EMA_21'] ) & ( data['EMA_9'].shift(1) > data['EMA_21'].shift(1) ) ],
            [2, -2])


        #########  Weighted SMA 20, 50  #####
        for i in [ 20, 50 ]:
            data = __WSMA ( data, i, cl=cl )

        data['WSMA_20_50_Signal'] = np.select(
            [ ( data['WSMA_20'] > data['WSMA_50'] ) & ( data['WSMA_20'].shift(1) < data['WSMA_50'].shift(1) ) ,
              ( data['WSMA_20'] < data['WSMA_50'] ) & ( data['WSMA_20'].shift(1) > data['WSMA_50'].shift(1) ) ],
            [2, -2])

        #########  WMA & Double WMA  ##### 
        for i in [ 9, 14, 20 ]:
            data = WMA ( data, i, cl=cl )


        #########  RSI 14 #####
        rsi_window      = 14
        rsi_overbought  = 70
        rsi_oversold    = 30

        data            = __RSI ( data, window=rsi_window )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['RSI_Signal'] = np.select(
            [ ( data['Trend_20'] > 1 ) & ( data['RSI_{}'.format(rsi_window)] > 40 ) & ( data['RSI_{}'.format(rsi_window)].shift(1) < 40),
            (   data['Trend_20'] < 1 ) & ( data['RSI_{}'.format(rsi_window)] < 60)  & ( data['RSI_{}'.format(rsi_window)].shift(1) > 60)],
            [2, -2])

        #########  W%R 20  #####
        wr_window      = 20
        wr_upper_level = -20
        wr_lower_level = -80

        data           = __WR ( data, wr_window, cl=cl )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['WR_Signal'] = np.select(
            [ ( data['WR_{}'.format(wr_window)].shift(1) > wr_upper_level ) & ( data['WR_{}'.format(wr_window)] < wr_upper_level ),
              ( data['WR_{}'.format(wr_window)].shift(1) < wr_lower_level ) & ( data['WR_{}'.format(wr_window)] > wr_lower_level )],
            [-2, 2])

        #########  TEMA 30 & 9  #####
        tema_window     = 30
        data            = __TEMA ( data, tema_window, cl=cl )
        data            = __TEMA ( data, 9, cl=cl )

        #########  STOCH  #####
        sto_k                = 14
        sto_d                = 3
        sto_slow             = 3
        sto_upper_level      = 80
        sto_lower_level      = 20

        data                 = __STOCHASTIC (data, sto_k, 3, cl=cl)

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['STO_Signal'] = np.select(
            [ ( data['STO_K'].shift(1) < sto_lower_level ) & ( data['STO_K'] > sto_lower_level ),
              ( data['STO_K'].shift(1) > sto_upper_level ) & ( data['STO_K'] < sto_upper_level ) ],
            [2, -2])

        #########  STOCHASTIC RSI  #####
        srsi_upper_level  = 80
        srsi_lower_level  = 20

        data             = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['SRSI_Signal'] = np.select(
            [ ( data['SRSI_K'].shift(1) < srsi_lower_level )  & ( data['SRSI_K'] > srsi_lower_level ),
              ( data['SRSI_K'].shift(1) > srsi_upper_level )  & ( data['SRSI_K'] < srsi_upper_level )],
            [2, -2])

        #########  CCI 20  #####
        cci_upper_level  =  100
        cci_lower_level  =  (-100)
        cci_window = 20

        data = __CCI (data, cci_window)

        data = __CCI ( data, 170 )
        data = __CCI ( data, 34 )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['CCI_Signal'] = np.select(
           [ ( data['CCI_{}'.format(cci_window)].shift(1) < cci_lower_level ) & ( data['CCI_{}'.format(cci_window)] > cci_lower_level ) ,
             ( data['CCI_{}'.format(cci_window)].shift(1) > cci_upper_level ) & ( data['CCI_{}'.format(cci_window)] < cci_upper_level ) ],
            [2, -2])


        data = __CCI ( data, 14 )
        data['CCI_Signal_14'] = np.select(
           [ ( data['CCI_14'].shift(1) < cci_lower_level ) & ( data['CCI_14'] > cci_lower_level ) ,
             ( data['CCI_14'].shift(1) > cci_upper_level ) & ( data['CCI_14'] < cci_upper_level ) ],
            [2, -2])


        #####  Bolinger Bands  #####
        bb_window = 20
        # Calculate the Bollinger Bands for the stock data
        data = __BB ( data, bb_window, cl=cl )

        #data['BB_percent'] = ( data[cl]    - data['BB_lower'] ) / ( data['BB_upper'] - data['BB_lower'] ) * 100
        #data['BB_sharp']   = ( data['BB_upper'] - data['BB_lower'] ) / ( data['BB_middle'] )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['BB_Signal'] = np.select(
            [ ( data[cl] < data['BB_lower'] ) & ( data[cl].shift(1) > data['BB_lower'].shift(1)),
            (   data[cl] > data['BB_upper'] ) & ( data[cl].shift(1) < data['BB_upper'].shift(1))],
            [2, -2])

        #########  MACD  #####
        data = __MACD (data, m=12, n=26, p=9, pc=cl)

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['MACD_Signal'] = np.select(
            [ ((data['MACD_HIST'] > 0 ) & ( data['MACD_HIST'].shift(1)<0)) ,
              ((data['MACD_HIST'] < 0 ) & ( data['MACD_HIST'].shift(1)>0))],
            [2, -2])


        #########  KDJ  #####
        data = __KDJ (data)

        #########  ATR BANDS  #####
        data = __ATR_BANDS ( data, 14 )

        atr_bands_upper = data['ATR_BANDS_UPPER'][-1]
        atr_bands_lower = data['ATR_BANDS_LOWER'][-1]

        #########  KC  #####
        data = __KC (data)

        #########  CMO  #####
        data = __CMO (data)

        #########  CMF  #####
        data = __CMF (data)

        #########  AO  #####
        data = __AO ( data, 5, 34 )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['AO_Signal'] = np.select(
            [ ( data['AO'] > 0 ) & ( data['AO'].shift(1) < 0 ),
            (   data['AO'] < 0 ) & ( data['AO'].shift(1) > 0 )],
            [2, -2])

        #########  MFI  #####
        mfi_window = 14
        mfi_upper_level = 75
        mfi_lower_level = 30
        data       = __MFI ( data, mfi_window )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['MFI_Signal'] = np.select(
            [ ( data['MFI_{}'.format(mfi_window)].shift(1) < mfi_lower_level ) & ( data['MFI_{}'.format(mfi_window)] > mfi_lower_level ) ,
              ( data['MFI_{}'.format(mfi_window)].shift(1) > mfi_upper_level ) & ( data['MFI_{}'.format(mfi_window)] < mfi_upper_level ) ],
            [2, -2])
        
        #########  ADX  #####
        data       = __ADX ( data , 14 )

        #########  MOM  #####
        data       = __MOM ( data, 14 )

        #########  TSI  #####
        data = __TSI ( data, 25, 13, 12)

        #########  ROC  #####
        data = __ROC ( data, 12, 6 )

        #########  PSAR  #####
        data = __PSAR ( data )


        ########################
        #####  STRATEGIES  #####
        ########################

        # A list of  messages for a ticker
        advice = []

        # Load strategy files from command line
        if args.strategies:
            for strategy_file in args.strategies:
                  with open ( 'strategies/' + strategy_file ) as f: exec(f.read())
                  

        # Load all strategy files from strategies/ folder
        else:
            path = 'strategies' 
            files = os.listdir(path)
            files_py = [i for i in files if i.endswith('.py')]
            files_py = sorted ( files_py )

            for strategy_file in files_py:
                #print ("Loading file: strategies/" + strategy_file)
                with open ( 'strategies/' + strategy_file ) as f: exec(f.read())

        #data.to_csv('data/{}_{}.csv'.format (ticker, interval), float_format='%.2f' )

        print ("\n")
        time.sleep(1)


        # check pandas dataframe columns for signals #
        sig_bull = []
        sig_bear = []
        # Iterate over the columns
        for column in data.columns:
            if column.endswith('_Signal'):
                signal_values = data[column]
                last_value = signal_values.iloc[-1]
                if last_value == 2:
                    bull = (f"{column}:BULL")
                    sig_bull.append(bull)
                elif last_value == -2:
                    bear = (f"{column}:BEAR")
                    sig_bear.append(bear)


        if ( len ( sig_bull ) > 0 ):
            print ( "Bull signals: \n" + '\n'.join ( sig_bull ) )

        if ( len ( sig_bear ) > 0 ):
            print ( "Bear signals: \n" + '\n'.join ( sig_bear ) )


    #print ( strategies )
    #print ( indicators )

    if ( args.refresh ):
        time.sleep ( int ( args.refresh ) )
    else:
        time.sleep ( int ( refresh ) )

