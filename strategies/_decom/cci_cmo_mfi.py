########################################
##### S5: CMCWiner: CCI, CMO, CMI  #####
########################################

data = __CCI ( data, 20 )
data = __MFI ( data )
data = __CMO ( data )

if ( ( data['CCI_20'][-1] < -100) &
    (  data['MFI_14'][-1] < 20) &
    (  data['CMO'][-1]    < -50)):
    print_log ( '24_CMCWinner', 'LONG', [ 'CMO', 'MFI', 'CCI_20' ] )

if ( ( data['CCI_20'][-1] > 100 ) &
    ( data['MFI_14'][-1]  > 80 ) &
    ( data['CMO'][-1]     > 50 )):
    print_log ( '24_CMCWinner', 'SHORT', [ 'CMO', 'MFI', 'CCI_20' ] )

