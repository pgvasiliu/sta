'''def aroon(Close, n=14):
    df = pd.DataFrame(Close)
    df['up'] = 100 * df['Close'].rolling(window=n + 1, center=False).apply(lambda x: x.argmax()) / n
    df['down'] = 100 * df['Close'].rolling(window=n + 1, center=False).apply(lambda x: x.argmin()) / n
    return (pd.Series(df['up']), pd.Series(df['down']))'''

df['Aroon Signal'] = np.select(
    [(df['Trend 50'] > 1) & (df['Aroon Up'] > 70) & (df['Aroon Up'].shift(1) < 70),
     (df['Trend 50'] < 1) & (df['Aroon Down'] > 70) & (df['Aroon Down'].shift(1) < 30)],
    [1, -1])

