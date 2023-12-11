# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# SMA 5, SMA 8
data = __SMA  ( data, 5 )
data = __SMA ( data, 8 )
data = __BB  ( data )

_vol   = data["Volume"].iloc[-1]

_rsi   = data["RSI_14"].iloc[-1]
_rsi_1 = data["RSI_14"].iloc[-2]



if ( _rsi >= 30 ) and ( _rsi_1 < 30 ) and ( data['TEMA_9'][-1] <= data['BB_middle'][-1] ) and ( data['TEMA_9'][-1] > data['TEMA_9'][-2] ) and ( _vol > 0):
    print_log ( '3_SMA', 'LONG', [ 'BB', 'RSI_14', 'TEMA_9' ] )

if ( _rsi >=70 ) and ( _rsi_1 < 70 ) and ( data['TEMA_9'][-1]  > data['BB_middle'][-1] )  and ( data['TEMA_9'][-1] < data['TEMA_9'][-2] ) and ( _vol > 0):
    print_log ( '3_SMA', 'SHORT', [ 'BB', 'RSI_14', 'TEMA_9' ] )



