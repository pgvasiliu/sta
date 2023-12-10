import pandas as pd
import numpy as np

#  WMA and Double WMA
def __DWMA(df, window, cl='Close'):
    weights = pd.Series(range(1,window+1))
    wma = df[cl].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    df['WMA_{}'.format(window)] = wma
    df['DWMA_{}'.format(window)] = df['WMA_{}'.format(window)].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    return df
