#################
#####  RSI  #####
#################

import pandas as pd
import numpy as np

"""
# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
#def RSI ( close, t ):
#    import talib
#    return talib.RSI ( close, timeperiod=t)

def __RSI ( data, window, cl='Close'):
    delta = data[cl].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI___{}'.format(window)] = rsi
    return data

"""

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):
    """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
        The TradingView code is as follows:
        //@version=4
        study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
        len = input(14, minval=1, title="Length")
        src = input(close, "Source", type = input.source)
        up = rma(max(change(src), 0), len)
        down = rma(-min(change(src), 0), len)
        rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
        plot(rsi, "RSI", color=#8E1599)
        band1 = hline(70, "Upper Band", color=#C0C0C0)
        band0 = hline(30, "Lower Band", color=#C0C0C0)
        fill(band1, band0, color=#9915FF, transp=90, title="Background")
    :param data:
    :param window:
    :param round_rsi:
    :return: an array with the RSI indicator values
    """

    delta = data["Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    # Define the overbought and oversold levels
    rsi_overbought = 70
    rsi_oversold = 30

    data['RSI_Crossover']  = np.where ( ( ( data['RSI_{}'.format ( window )].shift(1) < rsi_oversold )   & ( data['RSI_{}'.format ( window )] > rsi_oversold ) ),   1, 0 )
    data['RSI_Crossunder'] = np.where ( ( ( data['RSI_{}'.format ( window )].shift(1) > rsi_overbought ) & ( data['RSI_{}'.format ( window )] < rsi_overbought ) ), 1, 0 )


    # 2 = LONG, -2 = SHORT
    #data['RSI_Signal'] = 0
    #data['RSI_Signal'] = np.select(
    #    [  ( data['RSI_14'].shift(1) < rsi_oversold )   & ( data['RSI_14'] > rsi_oversold ),
    #       ( data['RSI_14'].shift(1) > rsi_overbought ) & ( data['RSI_14'] < rsi_overbought )],
    #    [2, -2])

    # Fisher RSI
    data['FRSI_{}'.format ( window )] = (np.exp(2 * rsi) - 1) / (np.exp(2 * rsi) + 1)

    return data

