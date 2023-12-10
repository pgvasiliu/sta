# ADX RSI https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies
'''
### Author:Vita ###
Strategy from:
https://forextester.com/blog/adx-14-ema-strategy
This strategy uses ADX and 14EMA for buy and sell signals
'''

data = __EMA ( data, 14 )
data = __ADX ( data, 14 )

if (data['Adj Close'].iloc[-1] > data["Open"].iloc[-1]) and ( data['Adj Close'].iloc[-1] > data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print_log ( 'adx_ema_14.py', 'LONG', [ 'ADX_14', 'EMA_14' ] )

# SELL CRITERIA: if candlestick is bearish, close is less than 14 EMA and ADX indicator has crossed above 25:
if ( data["Open"].iloc[-1] > data['Adj Close'].iloc[-1]) and ( data['Adj Close'].iloc[-1] < data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print_log ( 'adx_ema_14.py', 'SHORT', [ 'ADX_14', 'EMA_14' ] )
