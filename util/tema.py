#########################
#####  PANDAS TEMA  #####
#########################

#def TEMA ( close, t):
#    import talib
#    return talib.TEMA(close, timeperiod=t)

def __TEMA(data, n=30, cl='Close'):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data[cl].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    data['TEMA_{}'.format(n)] = tema
    return data
