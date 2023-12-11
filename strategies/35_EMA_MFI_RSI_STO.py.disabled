###############################################
#####  S35: EMA_MFI_RSI_STO Strategy 003  #####
###############################################
data = __SMA ( data, 40 )

data = __EMA ( data, 5 )
data = __EMA ( data, 10 )
data = __EMA ( data, 50 )
data = __EMA ( data, 100 )
data = __RSI ( data, 14 )
data = __MFI ( data, 14 )

if ( (  data['RSI_14'][-1]     < 28)
    & ( data['RSI_14'][-1]     > 0)
    & ( data['Adj Close'][-1]      < data['SMA_40'][-1] )
    & ( data['FRSI_14'][-1]    < -0.94)
    & ( data['MFI_14'][-1]     < 16.0) 
    & ( ( data['EMA_50'][-1]   > data['EMA_100'][-1] ) | ( ( data['EMA_5'][-1] > data['EMA_10'][-1] ) & ( data['EMA_5'][-2] < data['EMA_10'][-2]) ) )
    & ( data['STO_D'][-1]      > data['STO_K'][-1] )
    & ( data['STO_D'][-1]      > 0) ):
    print_log ( '35_EMA_MFI_RSI_STO', 'LONG', [ 'EMA_5', 'EMA_15', 'EMA_50', 'EMA_100', 'RSI_14', 'MFI_14' ] )


if ( ( data['PSAR'][-1] > data['Adj Close'][-1] ) ):
    # &(  data['fisher_rsi'] > 0.3) ):
    print_log ( '35_EMA_MFI_RSI_STO', 'SHORT', [ 'EMA_5', 'EMA_15', 'EMA_50', 'EMA_100', 'RSI_14', 'MFI_14' ] )


