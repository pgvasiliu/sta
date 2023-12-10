#import yfinance as yf
import pandas as pd

########################
#####  PANDAS MOM  #####
########################

#def __MOM (data, window=14):
#
#    # Calculate the Momentum (MOM) indicator
#    mom = pd.Series(data["Close"]).diff(window)
#
#    # Add the MOM indicator to the DataFrame
#    data["MOM_14"] = mom
#
#    return data

#Momentum
def __MOM(data, window=14, cl='Close'):
    mom = pd.Series(data[cl].diff(window), name = 'MOM_' + str(window))

    data['MOM_{}'.format(window)] = mom

    #data = data.join(M)
    return data

