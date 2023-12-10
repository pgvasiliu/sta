# CCI MA
"""
@author: mingyu and caitlin
This strategy combines the CCI, the commodity channel index with a simple moving average for 100 periods.
The CCI is a trend indicator that shows oversold and overbought conditions. Combine with the sma100
to attempt to filter some false signals.
"""

data['average'] = (data['High'] + data['Low'] + data['Adj Close']) / 3
data['period_100_average'] = data['average'].rolling(window=100).mean()

# A buy entry signal is when cci left oversold zone, i.e. just above -100, and price intersects the period 100 moving average from below
if data['CCI_20'].iloc[-1] > -100 and data['CCI_20'].iloc[-2] <= -100 and data['Adj Close'].iloc[-1] > data['period_100_average'].iloc[-1] and data['Adj Close'].iloc[-2] <= data['period_100_average'].iloc[-2]:
    print_log ( '45_MQL5_cci_moving_average.py', 'LONG', [ 'CCI_20', 'SMA_100' ] )

# A sell entry signal is when cci left overbought zone, i.e. just below 100, and price intersects the period 100 moving average from above
if data['CCI_20'].iloc[-1] < 100 and data['CCI_20'].iloc[-2] >= 100 and data['Adj Close'].iloc[-1] < data['period_100_average'].iloc[-1] and data['Adj Close'].iloc[-2] >= data['period_100_average'].iloc[-2]:
    print_log ( '45_MQL5_cci_moving_average.py', 'SHORT', [ 'CCI_20', 'SMA_100' ] )
