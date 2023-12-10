import numpy
import pandas

def hammer(ohlc_df):    
    """returns dataframe with hammer candle column"""
    df = ohlc_df.copy()
    df["hammer"] = (((df["High"] - df["Low"])>3*(df["Open"] - df["Close"])) & \
                   ((df["Close"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6) & \
                   ((df["Open"] - df["Low"])/(.001 + df["High"] - df["Low"]) > 0.6)) & \
                   (abs(df["Close"] - df["Open"]) > 0.1* (df["High"] - df["Low"]))
    return df

#def is_inverted_hammer( data ):
#    Open = data["Open"]
#    high = data["High"]
#    low  = data["Low"]
#    close = data["Close"]
#
#    return (high - close) > 2 * (close - low) and (high - Open) > 0.6 * (high - low)



