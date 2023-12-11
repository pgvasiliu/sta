########################
#####  STOCHASTIC  #####
########################

#def calculate_stochastic(df, k, d, slow, cl='Close'):
#    low = df['Low'].rolling(window=k).min()
#    high = df['High'].rolling(window=k).max()
#    df['K'] = (df[cl] - low) / (high - low) * 100
#    df['D'] = df['K'].rolling(window=d).mean()
#    df['Slow'] = df['D'].rolling(window=slow).mean()
#    return df

# https://github.com/Dynami/py-shibumi/blob/master/utils/technical_analysis.py
#Stochastic oscillator %K
#def STOK( df, cl='Close' ):
#    SOk = pd.Series((df[cl] - df['Low']) / (df['High'] - df['Low']), name = 'SO%k')
#    df = df.join(SOk)
#    return df

#Stochastic oscillator %D
#def STO(df, n, cl='Close'):
#    SOk = pd.Series((df[cl] - df['Low']) / (df['High'] - df['Low']), name = 'SO%k')
#    SOd = pd.Series(pd.ewma(SOk, span = n, min_periods = n - 1), name = 'SO%d_' + str(n))
#    df = df.join(SOd)
#    return df

## Stochastic Oscillator, EMA smoothing, nS = slowing (1 if no slowing)
#def STO(df,  nK, nD, nS=1, cl='Close'):
#    SOk = pd.Series((df[cl] - df['Low'].rolling(nK).min()) / (df['High'].rolling(nK).max() - df['Low'].rolling(nK).min()), name = 'SO%k'+str(nK))
#    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SO%d'+str(nD))
#    SOk = SOk.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()
#    SOd = SOd.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()
#    df = df.join(SOk)
#    df = df.join(SOd)
#    return df
## Stochastic Oscillator, SMA smoothing, nS = slowing (1 if no slowing)
#def STO(df, nK, nD,  nS=1, cl='Close'):
#    SOk = pd.Series((df[cl] - df['Low'].rolling(nK).min()) / (df['High'].rolling(nK).max() - df['Low'].rolling(nK).min()), name = 'SO%k'+str(nK))
#    SOd = pd.Series(SOk.rolling(window=nD, center=False).mean(), name = 'SO%d'+str(nD))
#    SOk = SOk.rolling(window=nS, center=False).mean()
#    SOd = SOd.rolling(window=nS, center=False).mean()
#    df = df.join(SOk)
#    df = df.join(SOd)
#    return df

def __STOCHASTIC (df, k, d, cl='Close'):

     temp_df = df.copy()

     # Set minimum low and maximum high of the k stoch
     low_min = temp_df["Low"].rolling(window=k).min()
     high_max = temp_df["High"].rolling(window=k).max()

     # Fast Stochastic
     temp_df['k_fast'] = 100 * (temp_df[cl] - low_min)/(high_max - low_min)
     temp_df['d_fast'] = temp_df['k_fast'].rolling(window=d).mean()

     # Slow Stochastic
     temp_df['STO_K'] = temp_df["d_fast"]
     temp_df['STO_D'] = temp_df['STO_K'].rolling(window=d).mean()

     temp_df = temp_df.drop(['k_fast'], axis=1)
     temp_df = temp_df.drop(['d_fast'], axis=1)


     return temp_df



