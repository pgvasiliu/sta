import pandas as pd
import numpy as np

def __WSMA( data, n, cl='Close'):
    weights = np.arange(1, n+1)
    wma = data[cl].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data

