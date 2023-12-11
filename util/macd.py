##################
#####  MACD  #####
##################

#def calculate_MACD(self,short_window, long_window, triger_line_days):
#        
#    data = copy.deepcopy(self.data)
#        
#    ewm_short = data['close'].ewm(span=short_window, adjust=False, min_periods=short_window).mean()
#    ewm_long = data['close'].ewm(span=long_window, adjust=False, min_periods=long_window).mean()
#        
#    macd = ewm_short - ewm_long  #MACD line
#    macd_s = macd.ewm(span=triger_line_days, adjust=False, min_periods=triger_line_days).mean() #MACD signal
#    macd_d = macd - macd_s #Difference
#        
#    run_name = '%s_%s_%s' %(short_window,long_window,triger_line_days)
#        
#    data['macd_' + run_name] = data.index.map(macd)
#    data['macd_s'+ run_name] = data.index.map(macd_s)
#    data['macd_d'+ run_name] = data.index.map(macd_d)
#    data = data[['macd_' + run_name,'macd_d'+ run_name,'macd_s'+ run_name]].round(4)

#def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
#    # Calculate the exponential moving averages (EMAs)
#    ema_fast = data["Close"].ewm(span=fast_period, adjust=False).mean()
#    ema_slow = data["Close"].ewm(span=slow_period, adjust=False).mean()
#
#    # Calculate the MACD line
#    macd_line = ema_fast - ema_slow
#
#    # Calculate the signal line
#    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
#
#    # Add the MACD and signal lines to the dataframe
#    data["MACD"] = macd_line
#    data["Signal"] = signal_line
#
#    return data

import numpy as np

##MACD, MACD Signal and MACD difference
#def MACD(df, n_fast, n_slow):
#    EMAfast = pd.Series(pd.ewma(df['close'], span = n_fast, min_periods = n_slow - 1))
#    EMAslow = pd.Series(pd.ewma(df['close'], span = n_slow, min_periods = n_slow - 1))
#    MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))
#    MACDsign = pd.Series(pd.ewma(MACD, span = 9, min_periods = 8), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))
#    MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))
#    df = df.join(MACD)
#    df = df.join(MACDsign)
#    df = df.join(MACDdiff)
#    return df

def __MACD (data, m=12, n=26, p=9, pc='Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    #data["MACD"] = data.apply(lambda x: (x["EMA_s"]-x["EMA_l"]), axis=1)
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    # Get the most recent day and the previous day in the dataframe
    #today_data = data.iloc[-1]
    #yesterday_data = data.iloc[-2]
    #data['MACD_Crossover']  = np.where ( ( (  yesterday_data["MACD"] <  yesterday_data["MACD_SIGNAL"] ) & ( today_data["MACD"] > today_data["MACD_SIGNAL"] ) ),   1, 0 )
    #data['MACD_Crossunder'] = np.where ( ( (  yesterday_data["MACD"] >  yesterday_data["MACD_SIGNAL"] ) & ( today_data["MACD"] < today_data["MACD_SIGNAL"] ) ), 1, 0 )

    ## Find the MACD crossover and crossunder
    #data['macd_crossover']  =  ( today_data["MACD"] > today_data["MACD_SIGNAL"] ) & ( yesterday_data["MACD"] <  yesterday_data["MACD_SIGNAL"] )
    #data['macd_crossunder'] = ( today_data["MACD"] < today_data["MACD_SIGNAL"] ) & ( yesterday_data["MACD"] >  yesterday_data["MACD_SIGNAL"] )

    #data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()

    #df['MACD_Signal'] = np.select(
    #    [ ( data['Trend_20'] > 1) & ( ( data['MACD_HIST'] > 0 ) & ( data['MACD_HIST'].shift(1) < 0 ) ) ,
    #      ( data['Trend_20'] < 1) & ( ( data['MACD_HIST'] < 0 ) & ( data['MACD_HIST'].shift(1) > 0 ) ) ],
    #    [2, -2])

    #data['MACD_Signal'] = np.select(
    #    [ ( ( data['MACD_HIST'] > 0 ) & ( data['MACD_HIST'].shift(1) < 0 ) ) ,
    #      ( ( data['MACD_HIST'] < 0 ) & ( data['MACD_HIST'].shift(1) > 0 ) ) ],
    #    [2, -2])

    return data

