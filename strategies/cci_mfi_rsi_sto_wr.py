data = __CCI ( data, 20 )
data = __RSI ( data, 14 )
data = __MFI ( data, 14 )
data = __STOCHASTIC ( data, 14, 3 )
data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )
data = __WR  ( data, 20 )

go_long  = 0
go_short = 0


# LONG #
if data['CCI_Signal'][-1] == 2:
   go_long += 1

if data['MFI_Signal'][-1] == 2:
   go_long += 1

if data['RSI_Signal'][-1] == 2:
   go_long += 1

if data['STO_Signal'][-1] == 2:
   go_long += 1

if data['SRSI_Signal'][-1] == 2:
   go_long += 1

if data['WR_Signal'][-1] == 2:
   go_long += 1


# SHORT #
if data['CCI_Signal'][-1] == -2:
   go_short += 1

if data['RSI_Signal'][-1] == -2:
   go_short += 1

if data['MFI_Signal'][-1] == -2:
   go_short += 1

if data['STO_Signal'][-1] == -2:
   go_short += 1

if data['SRSI_Signal'][-1] == -2:
   go_short += 1

if data['WR_Signal'][-1] == -2:
   go_short += 1


# go LONG if 3 out of 5 indicators flag oversold level and crossing up from below
if ( go_long >= 3 ):
   print_log ( 'cci_mfi_rsi_sto_wr.py', 'LONG', [ 'CCI', 'MFI', 'RSI', 'STOCHASTIC', 'SRSI', 'WR' ] )

# go SHORT if 3 out of 5 indicators flag overbought level and crossing down from above
if ( go_short >= 3 ):
   print_log ( 'cci_mfi_rsi_sto_wr.py', 'SHORT', [ 'CCI', 'MFI', 'RSI', 'STOCHASTIC', 'SRSI', 'WR' ] )

