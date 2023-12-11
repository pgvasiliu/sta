import os,sys
import numpy as np

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

# def __SMA ( df['Close'], 21 )
from util.sma   import __SMA

####################################
#####  PANDAS BOLLINGER BANDS  #####
####################################
#def calculate_bollinger_bands(data, window=20):
#    rolling_mean = data['Close'].rolling(window=window).mean()
#    rolling_std = data['Close'].rolling(window=window).std()
#    upper_band = rolling_mean + 2 * rolling_std
#    lower_band = rolling_mean - 2 * rolling_std
#    return rolling_mean, upper_band, lower_band

def __BB (data, window=20, cl='Close'):
    std = data[cl].rolling(window).std()
    data = __SMA ( data, window, cl )
    data['BB_upper']   = data["SMA_20"] + std * 2
    data['BB_lower']   = data["SMA_20"] - std * 2
    data['BB_middle']  = data["SMA_20"]

    # Calculate the cross over and cross under values
    #data['BB_Cross_Over']  = np.where ( data['Close'] > data['BB_upper'], 1, 0 )
    #data['BB_Cross_Under'] = np.where ( data['Close'] < data['BB_lower'], 1, 0 )

    ## 2 = LONG, -2 = SHORT
    #data['BB_Signal'] = np.select(
    #    [ ( data['Close'] < data['BB_lower'] ) & ( data['Close'].shift(1) > data['BB_lower'].shift(1)),
    #      ( data['Close'] > data['BB_upper'])  & ( data['Close'].shift(1) < data['BB_upper'].shift(1))],
    #    [2, -2])


    return data
