##########################################
#####  S34: BB_STO_RSI Strategy 002  #####
##########################################
#data = hammer ( data )
#hammer = data["hammer"]

data = __RSI ( data, 14 )
data = __STOCHASTIC ( data, 14, 3 )
data = __BB ( data )
data = __PSAR ( data )

#if ( is_hammer ( data ) & ( r_data["Close"][0] > r_data["Close"][1] ) ):
#    print ( f"{ticker} {interval} ---> Hammer\n")

if ( (  data['RSI_14'][-1]   < 30) 
    & ( data['STO_K'][-1]    < 20)
    & ( data['BB_lower'][-1] > data['Adj Close'][-1] ) ):
    #& ( hammer == True) ):
    print_log ( '34_BB_RSI_STO', 'LONG', [ 'RSI_14', 'STO', 'BB', 'PSAR' ] )

if ( ( data['PSAR'][-1]      > data['Adj Close'][-1] ) ):
#    & ( r_data['fisher_rsi'][0] > 0.3)):
    print_log ( '34_BB_RSI_STO', 'SHORT', [ 'RSI_14', 'STO', 'BB', 'PSAR' ] )
