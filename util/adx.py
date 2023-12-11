# IMPORTING PACKAGES

import numpy as np
import pandas as pd

def __ADX ( data, lookback):
    high = data["High"]
    low = data["Low"]
    close = data["Close"]
    open = data["Open"]

    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()

    data['ADX_{}_plus_di'.format(lookback)] = plus_di
    data['ADX_{}_minus_di'.format(lookback)] = minus_di
    #data['ADX_smooth'.format(lookback)] = adx_smooth
    #data["ADX"] = adx_smooth
    data['ADX_{}'.format(lookback)] = adx_smooth
    return data



