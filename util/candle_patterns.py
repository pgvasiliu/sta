##############################
#####  CANDLE  PATTERNS  #####
##############################
# https://github.com/nathanmcmillan/napa-bot/blob/b69a43bc994942be2b633295abcb7a954e26fcc4/python/patterns.py #
#def hammer(o,c,h,l):
#    body = abs(o - c)
#    wick = abs(min(o, c ) - l)
#    if wick > body * 2.0:
#        if is_close(c, h):
#            return 'green'
#        elif is_close(o, h):
#            return 'red'
#    return 'NA'


def hammer(ohlc_df):    
    """returns dataframe with hammer candle column"""
    df = ohlc_df.copy()
    df["hammer"] = (((df["High"] - df["Low"])>3*(df["Open"] - df["Close"])) & \
                   ((df["Close"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6) & \
                   ((df["Open"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6)) & \
                   (abs(df["Close"] - df["Open"]) > 0.1* (df["High"] - df["Low"]))
    return df

def shooting_star(candle):
    body = abs(candle.open - candle.closing)
    wick = abs(max(candle.open, candle.closing) - candle.high)
    if wick > body * 2.0:
        if is_close(candle.open, candle.low):
            return 'green'
        elif is_close(candle.closing, candle.low):
            return 'red'
    return ''

def marubozu(candle):
    if is_close(candle.open, candle.low) and is_close(candle.closing, candle.high):
        return 'green'
    if is_close(candle.open, candle.high) and is_close(candle.closing, candle.low):
        return 'red'
    return ''


def trend(candles, start, end):
    if candles[end].closing > candles[start].closing:
        return 'green'
    return 'red'


def change(candles, start, end):
    return abs(candles[end].closing - candles[start].closing) / candles[start].closing


def volume_trend(candles, start, end):
    if candles[end].volume > candles[start].volume:
        return 'green'
    return 'red'


def color(candle):
    if candle.closing > candle.open:
        return 'green'
    return 'red'

