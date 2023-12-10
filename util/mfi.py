import numpy as np

def __MFI ( data, window=14, cl='Close'):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data[cl]) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data['MFI_{}'.format(window)] = mfi

    # Define the overbought and oversold levels
    mfi_overbought = 75
    mfi_oversold   = 30

    data['MFI_Crossover']  = np.where ( ( ( data['MFI_{}'.format(window)].shift(1)  < mfi_oversold )   & ( data['MFI_{}'.format(window)] > mfi_oversold ) ),   1, 0 )
    data['MFI_Crossunder'] = np.where ( ( ( data['MFI_{}'.format(window)].shift(1)  > mfi_overbought ) & ( data['MFI_{}'.format(window)] < mfi_overbought ) ), 1, 0 )

    # 2 = LONG, -2 = SHORT
    #data['MFI_Signal'] = np.select(
    #    [ ( data['MFI_{}'.format(window)].shift(1)  < mfi_oversold )   & ( data['MFI_{}'.format(window)] > mfi_oversold ) ,
    #      ( data['MFI_{}'.format(window)].shift(1)  > mfi_overbought ) & ( data['MFI_{}'.format(window)] < mfi_overbought ) ],
    #    [2, -2])


    return data

