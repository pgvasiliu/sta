import pandas as pd
import numpy as np

def __CCI(df, ndays = 20, cl='Close'):
    df['TP'] = (df['High'] + df['Low'] + df[cl]) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: np.abs(x - x.mean()).mean())

    df['CCI_{}'.format(ndays)] = (df['TP'] - df['sma']) / (0.015 * df['mad'])



    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    return df
