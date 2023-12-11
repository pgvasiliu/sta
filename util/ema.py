#####  EMA  #####

#def EMA(close, t):
#    import numpy as np
#    import talib
#    return talib.EMA ( np.array(close), t)

def __EMA ( data, n=9, cl='Close' ):
    data['EMA_{}'.format(n)] = data[cl].ewm(span = n ,adjust = False).mean()
    return data

