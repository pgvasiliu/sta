# MACDStochasticCrossover
"""
@author: vita
This strategy uses the MACD crossovers and Stochastic crossovers. The stochastic crossover should occur just before the MACD crossover.
https://www.dailyfx.com/forex/education/trading_tips/daily_trading_lesson/2020/02/11/macd-vs-stochastic.html
"""

#close = data['Adj Close']
#high = data['High']
#low = data['Low']

data = __MACD ( data )
data = __STOCHASTIC ( data, 14, 3 )

m_line = data['MACD']
m_signal = data['MACD_SIGNAL']
k_line = data['STO_K']
d_signal = data['STO_D']

# BUY CRITERIA: stoch %k and %d lines crossover that are <20 shortly before MACD signal and line crossover that are <0
if (k_line.iloc[-3] < 20 and d_signal.iloc[-3] < 20 and k_line.iloc[-2] < 20 and d_signal.iloc[-2] < 20) and \
    ((k_line.iloc[-3] > d_signal.iloc[-3] and k_line.iloc[-2] < d_signal.iloc[-2])) and \
    (m_line.iloc[-2] < 0 and m_signal.iloc[-2] < 0 and m_line.iloc[-1] < 0 and m_signal.iloc[-1] < 0) and \
    (m_line.iloc[-2] < m_signal.iloc[-2] and m_line.iloc[-1] > m_signal.iloc[-1]):
    print_log ( '54_MQL5_macd_stochastic_crossover.py', 'LONG', [ 'MACD', 'STO' ] )

# SELL CRITERIA: stoch %k and %d lines crossover that are >80 shortly before MACD signal and line crossover that are >0
if (k_line.iloc[-3] > 80 and d_signal.iloc[-3] > 80 and k_line.iloc[-2] > 80 and d_signal.iloc[-2] > 80) and \
    ((k_line.iloc[-3] < d_signal.iloc[-3] and k_line.iloc[-2] > d_signal.iloc[-2])) and \
    (m_line.iloc[-2] > 0 and m_signal.iloc[-2] > 0 and m_line.iloc[-1] > 0 and m_signal.iloc[-1] > 0) and \
    (m_line.iloc[-2] > m_signal.iloc[-2] and m_line.iloc[-1] < m_signal.iloc[-1]):
    print_log ( '54_MQL5_macd_stochastic_crossover.py', 'SHORT', [ 'MACD', 'STO' ] )
