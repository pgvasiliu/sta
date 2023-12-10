import pandas as pd
import numpy as np

# def __RSI ( df, 14 )
from util.rsi   import __RSI

def __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3):
    # RSI
    data = __RSI ( data, period)

    # Stochastic RSI
    stochrsi  = (data['RSI_14'] - data['RSI_14'].rolling(period).min()) / (data['RSI_14'].rolling(period).max() - data['RSI_14'].rolling(period).min())
    data['SRSI_K'] = stochrsi.rolling(SmoothK).mean() * 100
    data['SRSI_D'] = data['SRSI_K'].rolling(SmoothD).mean()
    return data


