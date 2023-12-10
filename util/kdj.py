#########################
#####  PANDAS  KDJ  #####
#########################
#def __KDJ (data, n=9, ph='High', pl='Low', pc='Close'):
#    data['max'] = data[ph].rolling(window=n).max()
#    data['min'] = data[pl].rolling(window=n).min()
#    data['rsv'] = (data[pc] - data['min']) / (data['max'] - data['min']) * 100
#
#    # data.dropna(inplace=True)
#
#    data['K'] = data['rsv'].ewm(com=2, adjust=False).mean()
#    data['D'] = data['K'].ewm(com=2, adjust=False).mean()
#    data['J'] = 3 * data['K'] - 2 * data['D']
#
#    data.drop(['max', 'min', 'rsv'], axis=1, inplace=True)
#
#    return data

import numpy as np

def __KDJ (data, cl='Close'):
    low_min = data['Low'].rolling(window=9).min()
    high_max = data['High'].rolling(window=9).max()
    rsv = (data[cl] - low_min) / (high_max - low_min) * 100

    # this is not compabible with tradingview TV
    #data['KDJ_K'] = rsv.rolling(window=3).mean()
    #data['KDJ_D'] = data['KDJ_K'].rolling(window=3).mean()

    # compatible with tradingview and webull
    data['KDJ_K'] = rsv.ewm(com=2, adjust=False).mean()
    data['KDJ_D'] = data['KDJ_K'].ewm(com=2, adjust=False).mean()

    data['KDJ_J'] = 3 * data['KDJ_K'] - 2 * data['KDJ_D']

    data['KDJ_Overbought'] = np.where(data['KDJ_K'] > 80, 1, 0)
    data['KDJ_Oversold'] = np.where(data['KDJ_K'] < 20, 1, 0)

    # Wait for confirmation
    #data['KDJ_LONG_Signal']  = np.where  ( (data['KDJ_K'] > data['KDJ_D']) & (data['KDJ_K'].shift(1) < data['KDJ_D'].shift(1)), 1, 0)
    #data['KDJ_SHORT_Signal'] = np.where ( (data['KDJ_K'] < data['KDJ_D']) & (data['KDJ_K'].shift(1) > data['KDJ_D'].shift(1)), 1, 0)

    # 2 = LONG, -2 = SHORT
    data['KDJ_Signal'] = np.select(
        [ ( data['KDJ_K'] > data['KDJ_D'] ) & ( data['KDJ_K'].shift(1) < data['KDJ_D'].shift(1) ) ,
          ( data['KDJ_K'] < data['KDJ_D'] ) & ( data['KDJ_K'].shift(1) > data['KDJ_D'].shift(1) ) ],
        [2, -2])


    return data

