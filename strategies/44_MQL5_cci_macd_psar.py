"""

@author: mingyu and caitlin

This strategy combines the commodity channel index CCI with the Moving Average Convergence Divergence MACD
and Parabolic Stop and Reversal PSAR indicator. The CCI is used to show oversold and overbought zones, while
the PSAR value is checked if it is above or below the candlesticks showing a down or uptrend respectively,
 and the macd histogram is checked if it crosses the macd line from below or above indicating to buy or sell.
"""


# A buy entry signal is when cci left oversold zone, i.e. just above -100, and macd histogram crosses above the macd line and the psar is below the chart
if data['CCI_20'].iloc[-1] > -100 and data['CCI_20'].iloc[-2] <= -100 and data['MACD_HIST'].iloc[-1] > data['MACD'].iloc[-1] and data['MACD_HIST'].iloc[-2] <= data['MACD'].iloc[-2] and data['PSAR'].iloc[-1] <= data['Low'].iloc[-1]:
    print_log ( '44_MQL5_cci_macd_psar', 'LONG', [ 'CCI_20', 'MACD', 'PSAR' ] )

# A sell entry signal is when cci left overbought zone, i.e. just below 100, and macd histogram crosses below the macd line and the psar is above the chart
if data['CCI_20'].iloc[-1] < 100 and data['CCI_20'].iloc[-2] >= 100 and data['MACD_HIST'].iloc[-1] < data['MACD'].iloc[-1] and data['MACD_HIST'].iloc[-2] >= data['MACD'].iloc[-2] and data['PSAR'].iloc[-1] >= data['High'].iloc[-1]:
    print_log ( '44_MQL5_cci_macd_psar', 'SHORT', [ 'CCI_20', 'MACD', 'PSAR' ] )
