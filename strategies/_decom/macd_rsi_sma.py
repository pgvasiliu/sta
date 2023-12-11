# MacdRsiSma
"""
@author: caitlin and vita
This strategy combines 3 different indicators: MACD, RSI and SMA in order to determine buy and sell signals
The Moving Average Convergence Divergence (MACD) is a trend following momentum indicator that displays
the relation between 2 moving averages. This strategy uses the macd signal and macd line, where the signal
line trails the macd.
The Relative Strength Index (RSI) is a momentum indicator measuring speed and change of price movements.
The 5 period simple moving average is good for short term trading.
The goal of combining these indicators is to determine more accurate buy/sell signals than any provide by themselves.
"""
data = __SMA ( data, 5 )
data = __MACD ( data )
data = __RSI ( data, 14 )

sma_5       = data['SMA_5']
macd_line   = data['MACD']
macd_signal = data['MACD_SIGNAL']
rsi         = data['RSI_14']
close       = data['Adj Close']

# buy if close price is higher than the moving average, rsi reads less than 30 and the macd line crosses up through macd signal line
if (  data["SMA_5"].iloc[-1] < data["Adj Close"].iloc[-1]) and ( data["MACD"].iloc[-2] < data["MACD_SIGNAL"].iloc[-2]) and \
    ( data["MACD"].iloc[-1] > data["MACD_SIGNAL"].iloc[-1]) and ( data["MACD"].iloc[-1] < 0 and data["RSI_14"].iloc[-1] < 30):
    print_log ( 'macd_rsi_sma.py', 'LONG', [ 'MACD', 'RSI_14', 'SMA_5' ] )

# sell if close price less than moving average, rsi reads over 70, and macd line crosses down through signal line
if (  data["Adj Close"].iloc[-1] < data["SMA_5"].iloc[-1] ) and ( data["MACD"].iloc[-1] > 0 and data["RSI_14"].iloc[-1] > 70) and \
    ( data["MACD"].iloc[-2] > data["MACD_SIGNAL"].iloc[-2]) and ( data["MACD"].iloc[-1] < data["MACD_SIGNAL"].iloc[-1]):
    print_log ( 'macd_rsi_sma.py', 'SHORT', [ 'MACD', 'RSI_14', 'SMA_5' ] )
