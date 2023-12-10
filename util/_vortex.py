#Vortex Indicator: http://www.vortexindicator.com/VFX_VORTEX.PDF
def Vortex(df, n):
    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df['high'].at[i + 1], df['close'].at[i] - min(df['low'].at[i+1], df['close'].at[i]))
        #Range = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df['high'].at[i+1] - df['low'].at[i]) - abs(df['low'].at[i+1] - df['high'].at[i])
        #Range = abs(df.get_value(i + 1, 'high') - df.get_value(i, 'low')) - abs(df.get_value(i + 1, 'low') - df.get_value(i, 'high'))
        VM.append(Range)
        i = i + 1
    VM = pd.Series(VM)
    TR = pd.Series(TR)
    VI = pd.Series(VM.rolling(center=False, window=n).sum() / TR.rolling(center=False, window=n).sum(), name = 'Vortex_' + str(n))
    #VI = pd.Series(pd.rolling_sum(pd.Series(VM), n) / pd.rolling_sum(pd.Series(TR), n), name = 'Vortex_' + str(n))
    df = df.join(VI)
    return df

