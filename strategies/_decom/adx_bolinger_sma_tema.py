# Optimal timeframe for the strategy
timeframe = '5m'

##########################
#####  S29: Quickie  #####
##########################
data = __TEMA ( data, 9 )
data = __SMA ( data, 50 )
data = __SMA ( data, 200 )

data = __ADX ( data, 14 )

if ( (data['ADX_14'][-1]  > 30) &
    ( data['TEMA_9'][-1]  < data['BB_middle'][-1] ) &
    ( data['TEMA_9'][-1]  > data['TEMA_9'][-2]) &
    ( data['SMA_200'][-1] > data['Adj Close'][-1] ) ):
    print_log ( 'adx_bolinger_sma_tema.py', 'LONG', [ 'ADX', 'bolinger', 'SMA_50', 'SMA_200', 'TEMA_9' ] )

if (  (  data['ADX_14'][-1]  > 70 )
    & (  data['TEMA_9'][-1]  > data['BB_middle'][-1] )
    & (  data['TEMA_9'][-1]  < data['TEMA_9'][-2] ) ):
    print_log ( 'adx_bolinger_sma_tema.py', 'SHORT', [ 'ADX', 'bolinger', 'SMA_50', 'SMA_200', 'TEMA_9' ] )

