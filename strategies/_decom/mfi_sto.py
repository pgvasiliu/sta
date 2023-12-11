"""
Created on Sun Sep 27 10:19:23 2020

@author: mingy
"""

data = __MFI ( data, 14 )
data = __STOCHASTIC ( data, 14, 3 )

#BUY SIGNAL: when MFI_14 and the STO_K indicator both leaves the oversold zone
if ( (data['MFI_14'][-1] > 20) & ( data['MFI_14'][-2] <= 20 ) & ( data['STO_K'][-1] > 20 ) & ( data['STO_K'][-2] <= 20)):
    print_log ( '55_MQL5_mfi_stochastic.py', 'LONG', [ 'MFI_14', 'STO' ] )

#SELL SIGNAL: when MFI_14 and the STO_K indicator both leaves the overbought zone
if ( ( data['MFI_14'][-1] < 80 ) & ( data['MFI_14'][-2] >= 80 ) & ( data['STO_K'][-1] < 80 ) & ( data['STO_K'][-2] >= 80) ):
    print_log ( '55_MQL5_mfi_stochastic.py', 'SHORT', [ 'MFI_14', 'STO' ] )
