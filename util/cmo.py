def __CMO ( data, periods=14, cl='Close' ):
    tp = (data['High'] + data['Low'] + data[cl]) / 3
    cmo = (tp - tp.shift(periods)) / (tp + tp.shift(periods)) * 100
    data['CMO'] = cmo
    return data

