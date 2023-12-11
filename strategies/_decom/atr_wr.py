# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# EMA 9
data            = __EMA ( data, 9 )
data            = __WR ( data, 20 )
data['ATR_14']  = __ATR ( data, 14 )

_vol      = data["Volume"].iloc[-1]
_open     = data["Open"].iloc[-1]
_close    = data["Adj Close"].iloc[-1]

ema_9     = data["EMA_9"].iloc[-1]
atr_14    = data['ATR_14'].iloc[-1]
atr_14_1  = data['ATR_14'].iloc[-2]

wr        = data["WR_20"].iloc[-1]
wr_1      = data["WR_20"].iloc[-2]

#####  (4) ATR_14  & W%R  #####
# To reduce the false signal, check the William %R value and should be on the oversold area and previously reach < -95
if ( ema_9 - ( 2 * atr_14) > _open ) and ( wr < -80) and ( wr_1 < -95 ) and ( _close > _open ):
    print_log ( '5_ATR_WR', 'LONG', [ 'EMA_9', 'EMA_20', 'ATR_14', 'WR_20', 'Close' ] )

# To reduce the false signal, check the William %R value and should be on the overbought area and previously reach > -5
if ( ema_9 + ( 2 * atr_14) < _close ) and ( wr > -20 ) and ( wr_1 > -5 ):
    print_log ( '5_ATR_WR', 'SHORT', [ 'EMA_9', 'EMA_20', 'ATR_14', 'WR_20', 'Close' ] )
