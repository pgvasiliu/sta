def __CMF ( df, window=20, cl='Close' ):
    close = df[cl]
    low = df['Low']
    high = df['High']
    volume = df['Volume']

    mfv = ( (close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= volume
    cmf = mfv.rolling(window).sum() / volume.rolling(window).sum()

    df["CMF"] = cmf

    return df

