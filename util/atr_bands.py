##############################
#####  PANDAS ATR BANDS  #####
##############################

from util.ema   import __EMA
from util.atr   import __ATR
from util.wwma  import wwma

"""
def calculate_ATR_bands(data, window=20, multiplier=2):
    #
    #Calculate the ATR (Average True Range) bands for the given data.
    #The ATR bands consist of an upper and a lower band, which are calculated
    #as the moving average of the high/low prices plus/minus the ATR times
    #a given multiplier.
    #
    # Calculate the True Range
    data['tr0'] = abs(data['High'] - data['Low'])
    data['tr1'] = abs(data['High'] - data['Close'].shift())
    data['tr2'] = abs(data['Low'] - data['Close'].shift())
    data['TR'] = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    data.drop(['tr0', 'tr1', 'tr2'], axis=1, inplace=True)

    # Calculate the ATR
    data['ATR'] = data['TR'].rolling(window=window).mean()

    # Calculate the upper and lower bands
    data['upper_band'] = data['High'].rolling(window=window).mean() + multiplier * data['ATR']
    data['lower_band'] = data['Low'].rolling(window=window).mean() - multiplier * data['ATR']

    return data[['Close', 'upper_band', 'lower_band']].iloc[window:]

data = calculate_ATR_bands(data)
"""

def __ATR_BANDS ( data, t=14, cl='Close' ):
    _open  = data['Open']
    _close = data[cl]
    _high  = data['High']
    _low   = data['Low']

    atr = __ATR( data, t)

    atr_multiplicator = 2.0
    atr_basis = __EMA ( data, 20, cl)

    atr_band_upper  = data["EMA_20"] + atr_multiplicator * atr
    atr_band_lower  = data["EMA_20"] - atr_multiplicator * atr
    atr_band_middle = data["EMA_20"]

    #return atr_band_lower[-1], atr_band_upper[-1], atr_band_middle[-1]
    data['ATR_BANDS_UPPER']  = data["EMA_20"] + atr_multiplicator * atr
    data['ATR_BANDS_LOWER']  = data["EMA_20"] - atr_multiplicator * atr
    data['ATR_BANDS_MIDDLE'] = data["EMA_20"]

    return data
