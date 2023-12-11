'''
@author: Caitlin
This strategy combines the keltner channels, with the stochastic signal line.

'''

# BUY SIGNAL: candle close is below lower keltner band, stochastic signal is <=30, psar is below the candle
if data['High'].iloc[-1] < data['KC_lower'].iloc[-1] and data['STO_K'].iloc[-1] < 30:
    print_log ( 'kc_stochastic.py', 'LONG', [ 'KC', 'STO' ] )

# SELL SIGNAL: candle close above upper keltner band, stochastic signal >= 70, psar below candle
if data['Low'].iloc[-1] > data['KC_upper'].iloc[-1] and data['STO_K'].iloc[-1] > 70:
    print_log ( 'kc_stochastic.py', 'SHORT', [ 'KC', 'STO' ] )
