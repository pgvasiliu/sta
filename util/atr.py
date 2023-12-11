import numpy as np
import pandas as pd

from util.wwma  import wwma

# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
def __ATR (df, n=14):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
def __ATR2 (df, n=14):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    data["ATR2"] = atr
    return data

# https://github.com/Dynami/py-shibumi/blob/master/utils/technical_analysis.py
#Average True Range
def __ATR3 (df, n):
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df['High'].at[i+1], df['Close'].at[i]) - min(df['Low'].at[i+1], df['Close'].at[i])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(ignore_na=False,span=n, adjust=True,min_periods=n).mean(), name = 'ATR_' + str(n))
    df = df.join(ATR)
    return df


def calculate_ATR(df_func):
    # Calculating ATR - Average True Range
    high_low = df_func['High'] - df_func['Low']
    high_close = np.abs(df_func['High'] - df_func['Close'].shift())
    low_close = np.abs(df_func['Low'] - df_func['Close'].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    df_func['ATR_14'] = true_range.rolling(14).sum()/14

    return df_func

