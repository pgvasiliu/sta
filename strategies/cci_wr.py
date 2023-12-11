data = __CCI ( data, 20 )
data = __WR  ( data, 20 )

go_long  = 0
go_short = 0


# LONG #
if data['CCI_Signal'][-1] == 2:
   go_long += 1

if data['WR_Signal'][-1] == 2:
   go_long += 1


# SHORT #
if data['CCI_Signal'][-1] == -2:
   go_short += 1


if data['WR_Signal'][-1] == -2:
   go_short += 1


# go LONG if 3 out of 5 indicators flag oversold level and crossing up from below
if ( go_long >= 2 ):
   print_log ( 'cci_wr.py', 'LONG', [ 'CCI', 'WR' ] )

# go SHORT if 3 out of 5 indicators flag overbought level and crossing down from above
if ( go_short >= 2 ):
   print_log ( 'cci_wr.py', 'SHORT', [ 'CCI', 'WR' ] )

